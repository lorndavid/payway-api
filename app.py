from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import requests
import time
import datetime
import json
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

app = Flask(__name__, static_folder='static')

ABA_LINK = "https://link.payway.com.kh/ABAPAYFB405176Y"
session = requests.Session()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/checkout")
def checkout():
    """ABA KHQR Official Checkout - Full Payway Integration"""
    return render_template("checkout.html")


@app.route("/static/<path:path>")
def send_static(path):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('static', path)


@app.route("/generate", methods=["POST"])
def generate():
    """Fast KHQR generation using Anajak API.
    Prefers official download_qr image URL (no local generation = faster).
    Falls back to local QR only if download_qr missing.
    """
    try:
        amount = request.json.get("amount")
        if amount is None:
            return jsonify({"success": False, "error": "amount is required"}), 400

        # Try up to 2 times (upstream can flake on ABA navigation occasionally)
        # Tight timeouts + faster retry for better perceived speed on free hosting / variable latency
        last_err = None
        data = None
        api_response = None
        for attempt in range(2):
            try:
                api_response = session.post(
                    "https://api.anajak.site/api/create-qr",
                    json={
                        "url": ABA_LINK,
                        "amount": float(amount)
                    },
                    timeout=12
                )
                data = api_response.json()
                if api_response.status_code == 200:
                    break
                last_err = data
            except Exception as e:
                last_err = str(e)
                

        if not api_response or api_response.status_code != 200:
            return jsonify({"success": False, "error": last_err or "upstream error"}), 400

        tran_id = data.get("status", {}).get("tran_id") or data.get("tran_id")
        client_id = data.get("client_id")
        qr_string = data.get("qr_string")

        # Extract merchant info defensively (real API uses transaction_summary)
        merchant = None
        amount_out = None
        currency = None
        ts = data.get("transaction_summary") or {}
        if ts:
            merchant = ts.get("merchant", {}).get("company")
            od = ts.get("order_details", {})
            amount_out = od.get("amount")
            currency = od.get("currency")

        result = {
            "success": True,
            "tran_id": tran_id,
            "client_id": client_id,
            "qr_string": qr_string,
            "expire_in_sec": data.get("expire_in_sec"),
            "merchant": merchant,
            "amount": amount_out,
            "currency": currency,
        }

        # FAST PATH: use official pre-generated QR image from ABA (fastest, no CPU/encode)
        download_qr = data.get("download_qr")
        if download_qr:
            result["qr_url"] = download_qr
        else:
            # Fallback: generate locally if official QR URL is missing
            import qrcode
            import base64
            from io import BytesIO
            qr = qrcode.make(qr_string or "")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            result["qr_url"] = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/check", methods=["POST"])
def check_payment():
    """Proxy to Anajak check-status. Returns meta with qr_scanned / payment_approved."""
    try:
        tran_id = request.json.get("tran_id")
        client_id = request.json.get("client_id")

        if not tran_id:
            return jsonify({"success": False, "error": "tran_id required"}), 400

        api_response = session.post(
            "https://api.anajak.site/api/check-status",
            json={
                "tran_id": tran_id,
                "client_id": client_id
            },
            timeout=10
        )

        return jsonify(api_response.json())

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/health")
def health():
    """Fast health check of this service + upstream Anajak."""
    try:
        r = requests.get("https://api.anajak.site/health", timeout=5)
        upstream = r.json() if r.status_code == 200 else {"error": r.text}
    except Exception as e:
        upstream = {"error": str(e)}
    return jsonify({
        "status": "ok",
        "upstream": upstream
    })


@app.route("/download-receipt")
def download_receipt():
    """Generate and return a clean PDF receipt styled like ABA Bank receipts.
    No custom HTML receipt UI is built on the frontend.
    """
    tran_id = request.args.get("tran_id", "N/A")
    merchant = request.args.get("merchant", "Merchant")
    amount = request.args.get("amount", "0")
    currency = request.args.get("currency", "KHR")
    paid_at_str = request.args.get("paid_at")

    try:
        if paid_at_str:
            paid_dt = datetime.datetime.fromisoformat(paid_at_str.replace("Z", "+00:00"))
        else:
            paid_dt = datetime.datetime.now()
        paid_time = paid_dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        paid_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate PDF in memory (ABA-style professional receipt)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header bar (ABA blue)
    c.setFillColor(HexColor("#003087"))
    c.rect(0, height - 85, width, 85, fill=1, stroke=0)

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 42, "ABA PAY")

    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 60, "Official Payment Receipt")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, height - 75, "KHQR Transaction via Anajak")

    # Body content
    c.setFillColor(HexColor("#000000"))
    y = height - 115

    c.setFont("Helvetica-Bold", 13)
    c.drawString(45, y, "Transaction Summary")
    y -= 22

    c.setFont("Helvetica", 10)

    # Details
    details = [
        ("Merchant", merchant),
        ("Amount Paid", f"{amount} {currency}"),
        ("Transaction ID", tran_id),
        ("Date & Time", paid_time),
        ("Payment Method", "KHQR (ABA Bank)"),
        ("Status", "COMPLETED"),
    ]

    for label, value in details:
        c.setFont("Helvetica", 10)
        c.drawString(45, y, f"{label}:")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(180, y, str(value))
        y -= 18

    # Highlighted amount box
    y -= 15
    c.setFillColor(HexColor("#e8f5e9"))
    c.roundRect(45, y - 55, width - 90, 65, 4, fill=1, stroke=0)

    c.setFillColor(HexColor("#2e7d32"))
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, y - 18, "TOTAL AMOUNT RECEIVED")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y - 45, f"{amount} {currency}")

    # Footer
    c.setFillColor(HexColor("#003087"))
    c.rect(0, 0, width, 95, fill=1, stroke=0)

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width / 2, 72, "Thank you for your payment!")

    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 55, "This is a computer-generated receipt from ABA Pay.")
    c.drawCentredString(width / 2, 42, "For any inquiries, please contact ABA Bank or your merchant.")
    c.drawCentredString(width / 2, 28, f"Reference: {tran_id}")

    c.save()
    buffer.seek(0)

    filename = f"ABA_Receipt_{tran_id}.pdf"
    return Response(
        buffer.getvalue(),
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


@app.route("/status-stream")
def status_stream():
    """Server-Sent Events for real-time payment status.
    This makes checking payment much faster and smoother than client polling.
    The server polls Anajak internally every ~0.8s (faster detection) and pushes updates only when status changes.
    No lag on the client, single efficient connection.
    """
    tran_id = request.args.get("tran_id")
    client_id = request.args.get("client_id")

    if not tran_id or not client_id:
        return Response("data: {\"error\":\"missing params\"}\n\n", mimetype="text/event-stream")

    def event_generator():
        last_meta = {}
        max_checks = 300  # ~4 minutes with faster polling

        for i in range(max_checks):
            try:
                resp = session.post(
                    "https://api.anajak.site/api/check-status",
                    json={"tran_id": tran_id, "client_id": client_id},
                    timeout=8
                )
                data = resp.json() if resp.status_code == 200 else {}
                meta = data.get("meta", {})

                current = {
                    "qr_scanned": bool(meta.get("qr_scanned")),
                    "payment_approved": bool(meta.get("payment_approved")),
                    "finished": bool(meta.get("finished")),
                    "raw": data  # include full for flexibility
                }

                # Only push when something actually changed
                if current != last_meta:
                    yield f"data: {json.dumps(current)}\n\n"
                    last_meta = current.copy()

                if current["payment_approved"] or current["finished"]:
                    break

            except Exception as e:
                # Send error but keep trying
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

            time.sleep(0.5)  # faster internal polling for quicker scan/approval detection while still polite to upstream

        # Final event
        yield "data: {\"done\": true}\n\n"

    return Response(
        event_generator(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # important for nginx/proxies
        }
    )


if __name__ == "__main__":
    # Respect PORT env var (required for Render.com, Heroku, etc. free hosting)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)