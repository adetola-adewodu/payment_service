Documentation
=============

Put a brief description of 'payment_service'.

Example post to braintree


curl -H "Content-Type:" -d '{"amount": "5000.00", "credit_card_number": "5555555555554444", "cvv":"123", "expiration_date": "12/2016"}'
 http://payment-service.herokuapp.com/braintree
