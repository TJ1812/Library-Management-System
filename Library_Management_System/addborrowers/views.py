from django.shortcuts import render
from django.db import connection
from .models import Borrower

cursor = connection.cursor()

def index(request):
	ssnexist = False
	message = ""
	if(request.method == "POST"):
		fname = request.POST['fname']
		ssn = request.POST['ssn']
		address = request.POST['address']
		phone = request.POST['phone']

		query = "SELECT Ssn FROM Borrower WHERE Ssn = '" + ssn + "'"
		cursor.execute(query)

		if(cursor.fetchone() != None):
			ssnexist = True
		else:
			query = 'INSERT INTO Borrower(Ssn,Bname,Address,Phone) VALUES("'+ ssn +'","'+ fname +'","'+ address +'","'+ phone +'");'
			cursor.execute(query)
			message = "Successfully added the borrower"

	return render(request,'addborrowers/index.html',{'ssnexist':ssnexist,'message':message})