import urllib2
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from BeautifulSoup import BeautifulSoup


# BookerVille Python API Integrator
#  This file will provide the skeleton for the python API that will integrate with BookerVille
#  All rights Reserved - MIT Licensced
#   John Peurifoy (Please send comments or suggestion to johnpeurifoy@yahoo.com)

# A Class that represents an individual property that is returned by Summary

class Property:
	def __init__(self,propid,accountId,lastUpdate,detailApiHtml = None):
		self.propid = propid  				#The Bookerville property ID
		self.accountId = accountId 			#The Bookerville account ID
		self.lastUpdate = lastUpdate 		#The last update
		self.detailApiHtml = detailApiHtml 	#The HTML access url
	def __str__(self):
		return self.propid + " : " + self.accountId

	def __repr__(self):
		return self.propid + " : " + self.accountId

#This method returns a list of property objects that are associated with the authKey
#Takes in your authKey and returns a list of owned property objects
#param: authKey        API authentication key
#return: list of Property objects

def getAllProperties(authKey):
	summaryString = 'https://www.bookerville.com/API-PropertySummary?s3cr3tK3y='
	request = summaryString + authKey
	req = urllib2.Request(request,headers={"Accept:" : "application/xml"})
	u = urllib2.urlopen(req)
	tree = ElementTree.parse(u)
	rootElem = tree.getroot()
	prop_list = rootElem.findall("Property")
	#return prop_list
	if (len(prop_list) <= 0):
		return None
	retVal = []
	for child in prop_list:
		htmllink = child.attrib['property_details_api_url']
		bkvAccount = child.attrib['bkvAccountId']
		propid = child.attrib['property_id']
		lastup = child.attrib['last_update']
		
		newProp = Property(propid,bkvAccount,lastup,htmllink)

		retVal.append(newProp)
	return retVal 

#This method takes in a given set of dates and place and returns a quote as a BeautifulSoup object
#params: 	authKey         API Authentication Key
#			propertyNum		BK property number
#			beginDate		Date in YYYY-MM-DD
#			endDate			Date in YYYY-MM-DD
#			adults			The number of adults
#			children		Number of children
#			guestEmail		Guest email
#			guestAddress	Guest address
#			City 			Guest city
#			state 			Guest state
#			country			Guest country
#			firstName		Guest first name
#			lastName		Guest last name
#			phone			Guest phone
#			zip				Guest zip
#			Company 		Guest company
#			channel 		Channel
#			operation		Operation - should be QUOTE for this
#return: A BeautifulSoup object of the QUOTE XML (see http://www.bookerville.com/APIBookingSpec)

def getQuote(authKey,propertyNum,beginDate,endDate,adults,children=0,guestEmail='johnpeurifoy.yahoo.com',guestAddress='Address!',city='City',state='State!',country='US',firstName='Joe',lastName='Biggs',phone='555',zip='65555',company="Company!",channel="Channel!",operation='QUOTE'):

	reqURL = "https://www.bookerville.com/API-Booking?s3cr3tK3y="+authKey
	xml_string = "<request><operation>"+operation +"</operation><company>"+company + "</company><channel>" + channel + "</channel><bkvPropertyId>"+str(propertyNum)+ "</bkvPropertyId><beginDate>"+beginDate+"</beginDate><endDate>"+endDate + "</endDate><adults>"+str(adults)+"</adults><children>"+str(children)+"</children><guestData><email>"+guestEmail +"</email><address>"+guestAddress + "</address><city>"+city+"</city><state>"+state+"</state><country>"+country+"</country><firstName>"+firstName+"</firstName><lastName>"+lastName+"</lastName><phone>"+str(phone)+"</phone><zip>"+str(zip)+"</zip></guestData></request>"
	req = urllib2.Request(url=reqURL, data=xml_string,headers={'Content-Type': 'application/xml'})
	response = urllib2.urlopen(req)
	val = response.read()
	y = BeautifulSoup(val)
	return y

#This method takes in a given set of dates and place and books the reservation. It returns the response as a BeautifulSoup object. Note I have not included the complete rate calculation for additional items. 
#params: 	authKey         API Authentication Key
#			propertyNum		BK property number
#			beginDate		Date in YYYY-MM-DD
#			endDate			Date in YYYY-MM-DD
#			adults			The number of adults
#			email 			Guest email
#			address	 		Guest address
#			city 			Guest city
#			zip				Guest zip
#			country			Guest country
#			firstName		Guest first name
#			lastName		Guest last name
#			phone			Guest phone
#			rent			Rent cost
#			bookurl 		The url of booking
#  			child 			Number of children
#			company 		Guest company
#			channel 		The marketing channel they heard you through
#			guestCom        Guest comments
#			overOc          Over Occupancy surcharge 
#			dis 			Discount
#			net 			Net Rent
#			stateTax 		State Tax (defaults to 13 for Florida)
#			countTax 		Count Tax (defaults to 0)
#			addItems 		AdditionItems. (label,amount,taxed[yes or no])
#			refund 			Refund amount
#			operation		Operation - should be ADD for this
#return: A BeautifulSoup object of the ADD XML (see http://www.bookerville.com/APIBookingSpec)

def getAdd(authKey,propertyNum,beginDate,endDate,adults,email,address,city,zip,country,firstName,lastName,phone,rent,bookurl,child=0,company="Company",channel="Channel",guestCom="",overOc=0,dis=0,net=0,stateTax=13,countTax=0,addItems=None,refund=0,operation="ADD"):
	reqURL = "https://www.bookerville.com/API-Booking?s3cr3tK3y="+authKey
	xml_string = "<request> <operation>"+operation+"</operation> <bkvPropertyId>"+propertyNum+"</bkvPropertyId> <address>"+address+"</address> <city>"+city+"</city> <company>"+company+"</company> <channel>"+channel+"</channel> <country>"+country + "</country> <email>"+email+"</email> <firstName>"+firstName+"</firstName> <lastName>" +lastName+"</lastName> <phone>"+phone+"</phone> <zip>"+str(zip)+"</zip> <beginDate>"+beginDate+"</beginDate> <endDate>"+endDate+"</endDate> <adults>"+str(adults)+"</adults> <children>"+str(child)+"</children> <guestComments>"+guestCom+"</guestComments> <rent>"+str(rent)+"</rent> <overOccupancySurcharge>"+str(overOc)+"</overOccupancySurcharge> <discount>"+str(dis)+"</discount> <netRent>"+str(net)+"</netRent> <taxes> <tax> <id>1</id> <label>State Tax</label> <amount>"+str(stateTax)+"</amount> </tax> <tax> <id>2</id> <label>County Tax</label> <amount>"+str(countTax)+"</amount> </tax> </taxes> "
	#additionalItems should be a list of tuples
	xml_addiitons = "<additionalItems>"
	for item in addItems:
		xml_additions = xml_additions + "<additionalItem>" + "<label>"+ item[0] +"</label> <amount>" + item[1] + "</amont><taxed>" + item[2] + "</taxed>"
	xml_additions = xml_additions + "</additionalItems>"
	final = "<securityDeposit> <type>Refundable|Waiver</type> <amount>"+str(refund)+"</amount> </securityDeposit> <bookingURL>"+bookurl+"</bookingURL> </request>"
	totalString = xml_string+xml_additions+final
	req = urllib2.Request(url=reqURL, data=totalString,headers={'Content-Type': 'application/xml'})
	response = urllib2.urlopen(req)
	val = response.read()
	y = BeautifulSoup(val)
	return y

#This method takes in a reservation and sends the request to cancel it. It will return the XMl as a beautifulSOup object.
#params: 	authKey         API Authentication Key
#			bkId			BK booking id number
#			propId 			The property ID
#			beginDate		Date in YYYY-MM-DD
#			endDate			Date in YYYY-MM-DD
#			operation		Operation - should be DELETE for this
#return: A BeautifulSoup object of the Remove XML (see http://www.bookerville.com/APIBookingSpec)

def getRemove(authKey,bkId,propId,beginDate,endDate,operation='DELETE'):
	xml_string = "<request><operation>"+operation+"</operation><bkvBookingId>"+str(bkId)+"</bkvBookingId><bkvPropertyId>"+str(propId)+"</bkvPropertyId><beginDate>"+beginDate + "</beginDate><endDate>"+endDate +"</endDate></request>"
	reqURL = "https://www.bookerville.com/API-Booking?s3cr3tK3y="+authKey
	req = urllib2.Request(url=reqURL, data=xml_string,headers={'Content-Type': 'application/xml'})
	response = urllib2.urlopen(req)
	val = response.read()
	y = BeautifulSoup(val)
	return y

#This method takes in payment information and passes it to the server. It will return the XMl as a beautifulSOup object.
#params: 	authKey         API Authentication Key
#			bookid			BK booking id number
#			payId 			The payment ID number
#  			datePaid		The date paid 
# 			amount 			The amount paid
#			operation		Operation - should be ADD or DELETE for this
#return: A BeautifulSoup object of the Payment XML (see http://www.bookerville.com/APIPaymentSpec)

def getPayment(authKey,bookid,payId,datePaid,amount,operation = 'ADD',refundPortion=0,venue='Venue'):
	paymentString = "https://www.bookerville.com/API-Payment?s3cr3tK3y="+authKey
	xml_string="<bookingPayment> <bkvBookingId>"+str(bookId)+"</bkvBookingId> <operation>"+operation+"</operation> <bkvBookingPaymentId>"+str(payId)+"</bkvBookingPaymentId> <datePaid>"+datePaid+"</datePaid> <type>"+type+"</type> <amount>"+str(amount)+"</amount> <refundableSecurityDepositPortion>"+str(refundPortion)+"</refundableSecurityDepositPortion> <depositVenue>"+venue+"</depositVenue> </bookingPayment>"
	req = urllib2.Request(url=reqURL, data=xml_string,headers={'Content-Type': 'application/xml'})
	response = urllib2.urlopen(req)
	val = response.read()
	y = BeautifulSoup(val)
	return y

#This method takes in payment information and passes it to the server. It will return the XMl as a beautifulSOup object.
#params: 	authKey         API Authentication Key
#			propertyNum		the bookerville propertyNumber
#return: A BeautifulSoup object of the Avaiability XML (see http://www.bookerville.com/APIAvailabilitySpec)

def getPropertyAvailability(authKey,propertyNum):
	propertyString = 'https://www.bookerville.com/API-PropertyAvailability?s3cr3tK3y=' + authKey + '&bkvPropertyId='+propertyNum
	req = urllib2.Request(propertyString,headers={"Accept:" : "application/xml"})
	u = urllib2.urlopen(req)
	val = u.read()
	y = BeautifulSoup(val)
	return y

#This method returns property details about the given room It will return the XMl as a beautifulSOup object.
#params: 	authKey         API Authentication Key
#			propertyNum		the bookerville propertyNumber
#return: A BeautifulSoup object of the Avaiability XML (see http://www.bookerville.com/APIPropertyDetailsSpec)

def getPropertyDetails(authKey,propertyNum):
	propertyString = 'https://www.bookerville.com/API-PropertyDetails?s3cr3tK3y=' + authKey + '&bkvPropertyId='+propertyNum
	req = urllib2.Request(propertyString,headers={"Accept:" : "application/xml"})
	u = urllib2.urlopen(req)
	val = u.read()
	y = BeautifulSoup(val)
	return y

