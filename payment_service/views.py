""" Cornice services.
"""
from cornice import Service
import braintree
import stripe
import json

# Create stripe keys
stripe.api_key = "sk_test_AP2VBnLI89bwW8K41ZmYqBHx"

braintreeService = Service(name='braintree', path='/braintree', description="Brain tree resources")
stripeService = Service(name='stripe', path='/stripe', description="Stripe resources")



# Braintree configuration
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'c97c7xgtm7p9mhny',
    'b6h83b422wzhmqxt',
    'c4ad467826ffbe6e471262df1cce8394'
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


@stripeService.post(content_type="application/json")
def post_stripe_token(request):

    json_data = json.loads(request.body)
    amount = json_data['amount']

    #print amount
    #
    #customer_id = json_data['customer_id']
    #card_id = postdata.get('card_id','')

    return {'amount':amount}


    #customer = stripe.Customer.retrieve("cus_4CgMqZZvGZJhSr")
    #card = customer.cards.retrieve("card_104Cj82EUbF8A9mXsoFkxFxS")
    #
    #charge = stripe.Charge.create(
    #  amount=int(amount*100),
    #  currency="ngn", # I can Change to naira if needed
    #  card=card,
    #  description="Example charge"
    #)
    #
    #
    #
    #if charge['card']['cvc_check']:
    #    transaction_id = charge.id[3:22]
    #    results = {'order_number': transaction_id, 'message': u'Money has been charged'}
    #
    #elif charge.balance_transaction:
    #    results = {'order_number': 0, 'message': charge.failure_message, 'code': charge.failure_code,
    #               'text': charge.description}
    #else:
    #    results = {'order_number': 0, 'message':charge.failure_message, 'errors': charge.errors}
    #return results