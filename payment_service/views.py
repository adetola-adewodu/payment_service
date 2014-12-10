""" Cornice services.
"""
from cornice import Service
import braintree
import stripe
import json

# Create stripe keys
stripe.api_key = "Put your key"

braintreeService = Service(name='braintree-credit-card', path='/card/add', description="Add credit card")
braintreeCreditService = Service(name='Braintree Payment Code', path='/card/payment_method_code', description="Payment Code")
stripeService = Service(name='stripe', path='/stripe', description="Stripe resources")



# Braintree configuration
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    "the_merchant_id",
    "the_public_key",
    "the_private_key"
)

@braintreeService.post()
def post_credit_info(request):
    token = ""

    cvv = ''
    credit_card_number = 0
    expiration_date = "1/15"

    json_data = json.loads(request.body)
    amount = json_data['amount']

    if 'cvv' in json_data:
        cvv = json_data['cvv']

    if 'credit_card_number' in json_data:
        credit_card_number = int(json_data['credit_card_number'])

    if 'expiration_date' in json_data:
        expiration_date = json_data['expiration_date']


    result = braintree.Transaction.sale({
          "amount": amount,
          "credit_card": {
            "number": credit_card_number,
            "expiration_date": expiration_date,
            "cvv": cvv
          }
    })

    if not result.is_success:
        print result.errors.deep_errors

    return {'success':result.is_success}


@braintreeCreditService.post()
def add_credit_card(request):

    params = json.loads(request.body)

    result = braintree.Customer.create({
        "credit_card": {
            "venmo_sdk_payment_method_code": params["payment_method_code"]
        }
    })

    return {'success':result.is_success}




@stripeService.post()
def post_stripe_token(request):

    params = json.loads(request.body)
    amount = 100

    token = params['stripeToken']


    charge = stripe.Charge.create(
      amount=int(amount*100),
      currency="usd", # I can change to naira if needed
      card=token,
      description="Example charge"
    )


    if charge['card']['cvc_check']:
        transaction_id = charge.id[3:22]
        results = {'transaction_number': transaction_id, 'message': u'transaction good'}
    elif charge.balance_transaction:
        results = {'order_number': 0, 'message': charge.failure_message, 'code': charge.failure_code,
                   'text': charge.description}
    else:
        results = {'order_number': 0, 'message':charge.failure_message, 'errors': charge.errors}
    return results
