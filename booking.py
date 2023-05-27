import json
from datetime import datetime
import smtplib
import random
from email.message import EmailMessage
#app logic and function codes are in the class of booking system
class BookingSystem :
	def __init__(self,person_name,person_email,address,menucard):
		self.person = person_name
		self.email = person_email
		self.address = address
		self.ordereditems = []
		self.Dishes = menucard
		self.wishinghim()
		
	# command line welcome message, display menu card and call dish selector
	def wishinghim(self):
		print("\n Hey,"+self.person + "\n Welcome to our Restaurant \n" )
		self.showMenucard()
		self.dishSelector()

	# Showing menucard.
	def showMenucard(self):
		print(" This is our Menu " )
		count=0
		#table header printing line here 
		print("{:_>55} \n".format('_'),
			"{:10}{:35}{:5}".format("Item No.","Items","Price (\u00A3)"),
			"\n{:_>55}".format('_'))
		for Dish in self.Dishes:
			print("{:<10}{:35}{:5}".format(count+1,Dish["Items"],Dish["Price"]))
			count+=1
		print("____________________________________________________ \n", 
		"The above menu can be used to place your order", "\n",
	 	"\n To select dish - type 'S' \n To edit order - type 'E'  \n To complete order - press 'K'","\n \n " )
	
	# home functions to ordering ,editing,and complete ordering
	def dishSelector(self):
		waitStillSay = True
		while waitStillSay:
			print("current total: "+str(self.currentRateItems())+"\u00A3")
			customer_decision = input("*****Enter your Choice: ")
			if customer_decision == "E" or customer_decision == "e" :
				self.editList()
			elif customer_decision == "S" or customer_decision == "s" :
				self.selectDishes()
			elif customer_decision == "K" or customer_decision == "k" :
				if self.toCompleteOrder() == True :
					self.finalSltDishs()
					waitStillSay = False
				
	# Edit option after ordered items and any corrections		
	def editList(self):
		#Showing ordered Items this codes.
		for orderItem in self.ordereditems:
			print(orderItem)
		print("_______________________________________ \n editor is on \n _______________________________________")
		editKey = int(input("Enter your want to edit Serial No: "))
		if editKey <= len(self.ordereditems):
			print("if you want to delete item type--'D' \n if you want to edit quality of item type-- 'Q'")
			choice = input("Type your Choice: ")
			if choice == "D" or choice == "d" :
				self.ordereditems.pop(editKey-1)
				print("sucessfully deleted!")
			if choice == "Q" or choice == "q" :
				quantity = int(input("Enter your Change Quantity of Dish: "))
				self.ordereditems[editKey-1]["Quantity"]=quantity 
				
				print("sucessfully changed Quantity! \n_______________________________________")
	
	
	def selectQuantity(self):
		try:
			quantity = int(input("Enter Quantity of Dish: "))
			return quantity
		except ValueError:
			print("Please enter number not a word!")
			return self.selectQuantity()

	# Select Dishes by serial number , ordering and mentioning quantiy.
	def selectDishes(self):
		for orderItem in self.ordereditems:
			print(orderItem)
		print("_______________________________________ \n Select your Dish \n_______________________________________")
		
		notFinished = True
		while notFinished:
			sltDishId= numInput("Enter Item No. : ")		
			if sltDishId <= len(self.Dishes):
				selDish = self.Dishes[sltDishId-1]
				quantity =  self.selectQuantity()				
				selDish["Quantity"]= quantity
				self.ordereditems.append(selDish)
				print("sucessfully registered \n_______________________________________")
				notFinished = False			
			else:
				print("Invalid Item")	
				notFinished = True

	#This outputs current list ordered pfrice
	def currentRateItems(self):
		total=0
		for items in self.ordereditems:
			peritem = items["Price"]*items["Quantity"]
			total+= peritem
		return total

	# completiion of order and send to final process of billing 
	def toCompleteOrder(self):
		print("Is your order complete? \n To Finish type --'Y' \n To continue type--'N'")
		confirmation = input("Type you decison: ")
		if confirmation == "Y" or confirmation == "y":
			print("Orders are registered!")
			return True
		if confirmation == "N" or confirmation == "n":
			return False

	# Editing frist entered mail and it will otp autheication process
	def editEmail(self):
		print("_______________________________________ \n Edit email ID \n_________________________________")
		changeEmail = input("Enter your new Email ID: ")
		Otp = genOtp()
		message = "it is your OTP: "+str(Otp)
		sender(changeEmail,"verification for change new email ID",message) 
		verify =input("Enter you Otp number recieved in mail: " )
		if verify == Otp:
			self.email = changeEmail

	# Final showing of ordered list and here can delete items and go to email process
	def finalSltDishs(self):
		count=0
		print("________________________________________________ \n Item No. --*-- Items--------*-- Price -------*-- Quantity")
		for orderItem in self.ordereditems:
			
			S,Is,Pe,Qy = str(count+1),orderItem["Items"],str(orderItem["Price"]),str(orderItem["Quantity"])
			print(" "+S+" --*-- "+Is+"--------*-- "+Pe+"\u00A3 -------*-- "+Qy+"-Qty")	
			count+=1
		print("********* total amount:"+str(self.currentRateItems())+"\u00A3 ******")
		print("\n Delivery address:"+str(self.address)+"\n")
		waittoconfirm = True
		while waittoconfirm:
			print("_____________________________________________________\n please confirm your email ID '"
	 		+self.email+"' as bill and payment option will be sent via email. \n To edit email id type--'M'",
			" \n To edit items type--'E' \n Show Ordered list again type--'S' \n Confirm Your final Order type--'O' ")
			choice = input("Enter your choice: ")
			if choice == "M" or choice == "m":
				self.editEmail()
			elif choice == "E" or choice == "e":
				self.editList()
			elif choice == "O" or choice == "o":
				self.finalisedItems()
				waittoconfirm =False
			elif choice =="S" or choice =="s":
				count =0
				for orderItem in self.ordereditems:
					S,Is,Pe,Qy = str(count+1),orderItem["Items"],str(orderItem["Price"]),str(orderItem["Quantity"])
					print(" "+S+" --*-- "+Is+"--------*-- "+Pe+"\u00A3 -------*-- "+Qy+"-Qty")	
					count+=1
				print("total price: "+str(self.currentRateItems())+"\u00A3")
			elif choice == "D" or choice == "d":
				exit()


#error handling codes here
def strInput(strings):
	while True:
		try:
			val = input(strings)
			break
		except ValueError:
			print("something went wrong")
		except KeyboardInterrupt:
			print("You pressed control-c, you want to quit? \n\n To quit press 'Q' \n To continue press 'C'")
			cho=strInput("Enter your choice: ")
			if cho=="Q" or cho =="q":
				exit()
			if cho =="C" or cho =="c":
				continue

	return val




def numInput(strings):
	while True:
		try:
			val = int(input(strings))
			break
		except ValueError:
			print("Please enter number not a word!")
		except KeyboardInterrupt:
			print("You pressed control-c ,you want to quit ? \n\n you want to quit press 'Q' you \n you want continue press 'C'")
			cho=strInput("enter your next step: ")
			if cho=="Q" or cho =="q":
				exit()
			if cho =="C" or cho =="c":
				continue

	return val



# 6 digit number random generate 					
def genOtp():
	val =""
	for i in range(0,6):
		ran=random.randrange(0, 10)
		val+=str(ran)
		
	return val

# mail  sender option
def sender( to_mail,subject,messages):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('hostemail','enter_your_apikey')
    emails = EmailMessage()
    emails['From'] =  'hostemail'
    emails['To'] = to_mail
    emails['Subject'] = subject
    emails.set_content(messages)
    server.send_message(emails)		


if __name__ == "__main__":
	
	print("\n ************ Welcome to online booking system ************",
       "\n \n To order food -- type 'y' \n To quit -- type 'n'")

	gateQuestion  = input(" \n type your choice: ")
	with open('menucard.json') as json_file:
		Dishes = json.load(json_file)
	if gateQuestion == "y" or gateQuestion == "Y" :
		print("\n ------------------------------------------")
		name = input("Enter your name: ")
		email  = input("Enter your email id: ")
		address = input("Enter your address: ")
		customer = BookingSystem(name,email,address,Dishes)
		
		
	elif gateQuestion == "n" or gateQuestion == "N" :
		exit()




	