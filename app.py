from flask import Flask, render_template, request
from bsedata.bse import BSE

app = Flask(__name__)

b = BSE(update_codes=True)  # Update the codes to fetch the latest data

# Stocks With Their Company Code and Average Price
stocks = {
    "Clean Science and Technology Ltd": {
        "code": "543318",
        "price": 1355.45,
        "quantity": 11,
        "average_price": 1578.92
    },
    "Avenue Supermarts Ltd": {
        "code": "540376",
        "price": 3678.05,
        "quantity": 3,
        "average_price": 3989.93
    },
    "Housing & Urban Development Corporation Ltd": {
        "code": "540530",
        "price": 60.65,
        "quantity": 86,
        "average_price": 56.49
    },
    "SUZLON ENERGY LTD": {
        "code": "532667",
        "price": 14.85,
        "quantity": 236,
        "average_price": 6.80
    },
    "PAYTM": {
        "code": "543396",
        "price": 835.65,
        "quantity": 17,
        "average_price": 1074.44
    },
    "ALLCARGO LOGISTICS LTD": {
        "code": "532749",
        "price": 290.50,
        "quantity": 13,
        "average_price": 172.12
    },
    "Gujarat Gas Ltd": {
        "code": "539336",
        "price": 484.30,
        "quantity": 20,
        "average_price": 537.51
    },
    "Heranba Industries Ltd": {
        "code": "543266",
        "price": 355.61,
        "quantity": 10,
        "average_price": 606.88
    },
    "NHPC LTD": {
        "code": "533098",
        "price": 45.25,
        "quantity": 48,
        "average_price": 41.13
    },
    "Rossari Biotech Ltd": {
        "code": "543213",
        "price": 841.75,
        "quantity": 10,
        "average_price": 1008.30
    },
    "Sumitomo Chemical India Ltd": {
        "code": "542920",
        "price": 413.29,
        "quantity": 40,
        "average_price": 398.21
    },
    "TTK PRESTIGE LTD": {
        "code": "517506",
        "price": 721.65,
        "quantity": 10,
        "average_price": 1011.69
    },
    "WIPRO LTD": {
        "code": "507685",
        "price": 394.25,
        "quantity": 19,
        "average_price": 576.24
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stock']
        purchase_price = float(request.form['purchase_price'])
        quantity = int(request.form['quantity'])
        average_price = float(request.form['average_price'])

        stocks[stock] = {
            "code": stock,
            "price": purchase_price,
            "quantity": quantity,
            "average_price": average_price
        }

    stock_data = []
    total_invested_amount = 0
    total_current_amount = 0

    for stock, details in stocks.items():
        code = details["code"]
        purchase_price = details["price"]
        quantity = details["quantity"]
        average_price = details["average_price"]

        quote = b.getQuote(code)
        current_price = float(quote.get("currentValue") or quote.get("lastPrice", 0.0))

        if current_price > purchase_price:
            profit = int((current_price - purchase_price) * quantity * 1.5)
            color = "green"
            status = f"Profit: {profit}"
            action = "Wait"
            action_color = "red"
        elif current_price == purchase_price:
            color = "black"
            status = "No Profit No Loss"
            action = "Wait"
            action_color = "red"
        elif purchase_price < current_price and current_price > average_price:
            profit = int((current_price - purchase_price) * quantity * 1.5)
            color = "green"
            status = f"Profit: {profit}"
            action = "Sell"
            action_color = "green"
        else:
            loss = int((purchase_price - current_price) * quantity)
            color = "red"
            status = f"Loss: {loss}"
            action = "Wait"
            action_color = "red"

        invested_amount = purchase_price * quantity
        current_amount = current_price * quantity

        total_invested_amount += invested_amount
        total_current_amount += current_amount

        stock_data.append({
            "stock": stock,
            "purchase_price": purchase_price,
            "quantity": quantity,
            "current_price": current_price,
            "average_price": average_price,
            "status": status,
            "color": color,
            "action": action,
            "action_color": action_color,
            "invested_amount": invested_amount,
            "current_amount": current_amount
        })

    return render_template('stock_information.html', stocks=stock_data, total_invested_amount=total_invested_amount, total_current_amount=total_current_amount)

if __name__ == '__main__':
    app.run()