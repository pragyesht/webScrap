from verify_email import verify_email

isvalid = verify_email('pragyesht@gmail.com', debug=True)

print(isvalid and 'valid' or 'not valid')
