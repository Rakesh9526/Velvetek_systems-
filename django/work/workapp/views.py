from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from .forms import ApplyForm,UserForm,FuelChargeForm,FoodAllowanceForm,ItemPurchasedForm,VendorInfoForm,CurrentStatusForm
from .models import Customer,Apply,FuelCharge,FoodAllowance,ItemPurchased,VendorInfo,CurrentStatus
from . import views
import requests
import urllib.parse
import re
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required





def index(request):
    technician_customers = None  
    
    if request.user.is_authenticated:
        technician_customers = Apply.objects.filter(service_by=request.user)

    context = {}
    if technician_customers:
        context['details'] = technician_customers
    
    return render(request, 'index.html', context)



def loginn(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'login.html',{'error': 'invalid username or password'})
    return render(request,'login.html')



def is_valid_phone_number(phone):
    return re.match(r"^\+\d{10,15}$", phone) is not None

def apply(request):
    details = None
    users = User.objects.all()  # Fetch all users, filter as needed
    
    # Fetch customer details by GET request
    if 'contact_number' in request.GET:
        contact_number = request.GET.get('contact_number', '').strip()
        try:
            details = Customer.objects.get(u_contact_number=contact_number)
        except Customer.DoesNotExist:
            messages.error(request, "No customer found with this contact number.")
            return redirect('apply')
    
    # Handle form submission via POST
    if request.method == "POST":
        contact_number = request.POST.get('contact_number')
        work_type = request.POST.get('work_type')
        item_name_or_number = request.POST.get('item_name_or_number')
        issue = request.POST.get('issue', '')
        photos_of_item = request.FILES.get('photos_of_item')
        estimation_document = request.FILES.get('estimation_document')
        estimated_price = request.POST.get('estimated_price', '')
        estimated_date = request.POST.get('estimated_date', '')
        any_other_comments = request.POST.get('any_other_comments', '')
        service_by_id = request.POST.get('service_by')  # Get selected service by ID
        
        try:
            customer = Customer.objects.get(u_contact_number=contact_number)
            service_by_user = User.objects.get(id=service_by_id)  # Fetch the User object
            
            Apply.objects.create(
                name=customer.u_name,
                address=customer.u_address,
                contact_number=customer.u_contact_number,
                whatsapp_number=customer.u_whatsapp_number,
                reffered_by=customer.u_reffered_by,
                work_type=work_type,
                item_name_or_number=item_name_or_number,
                issue=issue,
                photos_of_item=photos_of_item,
                estimation_document=estimation_document,
                estimated_price=estimated_price,
                estimated_date=estimated_date,
                any_other_comments=any_other_comments,
                service_by=service_by_user,  # Assign the User object
            )
            messages.success(request, "Application submitted successfully!")
            return redirect('apply')
        except Customer.DoesNotExist:
            messages.error(request, "Invalid customer contact number.")
        except User.DoesNotExist:
            messages.error(request, "Invalid service by user.")
    
    context = {
        'details': details,
        'users': users,
    }
    return render(request, 'apply.html', context)




def user(request):
    if 'term' in request.GET:
        term = request.GET.get('term', '').strip()
        qs = Customer.objects.filter(u_contact_number__istartswith=term)
        u_contact_numbers = [contact.u_contact_number for contact in qs]
        return JsonResponse(u_contact_numbers, safe=False)

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        whatsapp = request.POST.get('whatsapp', '').strip()
        referred_by = request.POST.get('referred_by', '').strip()

        if not name or not contact_number:
            messages.error(request, "Name and Contact Number are required.")
            return render(request, 'addcustomer.html')

        if Customer.objects.filter(u_contact_number=contact_number).exists():
            messages.error(request, "A customer with this contact number already exists.")
            return render(request, 'addcustomer.html')

        Customer.objects.create(
            u_name=name,
            u_address=address,
            u_contact_number=contact_number,
            u_whatsapp_number=whatsapp,
            u_reffered_by=referred_by,
        )

        messages.success(request, "Customer added successfully!")
        customers = Customer.objects.all()
        return render(request, 'newcustomer.html', {'success': True, 'customers': customers})

    return render(request, 'addcustomer.html')


def newcustomer(request):
    dict_user={
        'customers':Customer.objects.all()
    }
    return render(request,'newcustomer.html',dict_user)






def fuelcharge(request, apply_id):
    try:
        # Fetch the Apply instance based on the given apply_id
        apply_instance = Apply.objects.get(id=apply_id)
    except Apply.DoesNotExist:
        messages.error(request, "Apply instance not found.")
        return redirect('apply_list')  # Replace with your appropriate redirect

    if request.method == "POST":
        # Retrieve form data
        technician_name = request.POST.get('technician_name')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        kilometers = request.POST.get('kilometers')
        cost = request.POST.get('cost')

        # Validate required fields
        if not all([technician_name, date, purpose, kilometers, cost]):
            messages.error(request, "All fields are required.")
            return redirect('fuelcharge', apply_id=apply_id)

        try:
            # Fetch customer_name and issue from Apply instance
            customer_name = apply_instance.name  # Adjust field name as per your model
            issue = apply_instance.issue  # Adjust field name as per your model

            # Save data to the FuelCharge model
            FuelCharge.objects.create(
                apply=apply_instance,
                technician_name=technician_name,
                date=date,
                purpose=purpose,
                kilometers=kilometers,
                cost=cost,
                customer_name=customer_name,  # Include customer name
                issue=issue  # Include issue
            )
            messages.success(request, "Fuel charge added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('fuelcharge', apply_id=apply_id)

        return redirect('fuelcharge', apply_id=apply_id)

    # Fetch all existing FuelCharge records for the Apply instance
    fuel_charges = FuelCharge.objects.filter(apply=apply_instance)

    return render(request, 'fuelcharge.html', {
        'apply': apply_instance,
        'fuel_charges': fuel_charges,
    })

def updatefuelcharge(request, fuel_id):
    # Get the FuelCharge instance or return a 404 error if not found
    fuel = get_object_or_404(FuelCharge, id=fuel_id)

    if request.method == "POST":
        # Retrieve form data
        technician_name = request.POST.get('technician_name')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        kilometers = request.POST.get('kilometers')
        cost = request.POST.get('cost')

        # Validate required fields
        if not all([technician_name, date, purpose, kilometers, cost]):
            messages.error(request, "All fields are required.")
            return redirect('updatefuelcharge', fuel_id=fuel_id)

        try:
            # Update and save the FuelCharge instance
            fuel.technician_name = technician_name
            fuel.date = date
            fuel.purpose = purpose
            fuel.kilometers = kilometers
            fuel.cost = cost
            fuel.save()

            messages.success(request, "Fuel charge updated successfully!")
            return redirect('fuelcharge', apply_id=fuel.apply.id)  # Redirect to the correct fuelcharge view
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('updatefuelcharge', fuel_id=fuel_id)

    # Pass the 'fuel' instance to the template for editing
    return render(request, 'updatefuelcharge.html', {'fuel': fuel})




def foodallowance(request, apply_id):
    try:
        # Fetch the Apply instance based on apply_id
        apply_instance = Apply.objects.get(id=apply_id)
    except Apply.DoesNotExist:
        messages.error(request, "Apply instance not found.")
        return redirect('apply_list')  

    if request.method == "POST":
        # Retrieve form data
        technician_name = request.POST.get('technician_name')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        cost = request.POST.get('cost')

        # Validate required fields
        if not all([technician_name, date, purpose, cost]):
            messages.error(request, "All fields are required.")
            return redirect('foodallowance', apply_id=apply_id)

        try:
            # Fetch customer_name and issue from Apply instance
            customer_name = apply_instance.name  # Adjust based on Apply model fields
            issue = apply_instance.issue  # Adjust based on Apply model fields

            # Save data to FoodAllowance model
            FoodAllowance.objects.create(
                apply=apply_instance,
                technician_name=technician_name,
                date=date,
                purpose=purpose,
                cost=cost,
                customer_name=customer_name,  # Include customer_name
                issue=issue  # Include issue
            )
            messages.success(request, "Food allowance added successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('foodallowance', apply_id=apply_id)

        return redirect('foodallowance', apply_id=apply_id)

    # Fetch all existing FoodAllowance records for the Apply instance
    food_allowances = FoodAllowance.objects.filter(apply=apply_instance)

    context = {
        'apply': apply_instance,
        'food_allowances': food_allowances
    }
    return render(request, 'foodallowance.html', context)

def updatefoodallowance(request, food_id):
    # Get the FoodAllowance instance or return a 404 error if not found
    food = get_object_or_404(FoodAllowance, id=food_id)

    if request.method == "POST":
        # Retrieve form data
        technician_name = request.POST.get('technician_name')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        cost = request.POST.get('cost')

        # Validation for required fields
        if not all([technician_name, date, purpose, cost]):
            messages.error(request, "All fields are required.")
            return render(request, 'updatefoodallowance.html', {'food': food})

        try:
            # Update and save the FoodAllowance instance
            food.technician_name = technician_name
            food.date = date
            food.purpose = purpose
            food.cost = cost
            food.save()

            messages.success(request, "Food allowance updated successfully!")
            return redirect('foodallowance', apply_id=food.apply.id)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'updatefoodallowance.html', {'food': food})

    # Pass the 'food' instance to the template for editing
    return render(request, 'updatefoodallowance.html', {'food': food})





def itempurchased(request, apply_id):
    try:
        # Fetch the Apply instance based on apply_id
        apply_instance = Apply.objects.get(id=apply_id)
    except Apply.DoesNotExist:
        messages.error(request, "Apply instance not found.")
        return redirect('apply_list')  # Redirect to an appropriate page

    if request.method == "POST":
        # Retrieve form data
        date = request.POST.get('date')
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        bill_photo = request.FILES.get('bill_photo')  # Handling file uploads

        # Validate required fields
        if not all([date, item_name, price, bill_photo]):
            messages.error(request, "All fields are required.")
            return redirect('itempurchased', apply_id=apply_id)

        try:
            # Fetch customer_name and issue from Apply instance
            customer_name = apply_instance.name  # Adjust field names as per Apply model
            issue = apply_instance.issue  # Adjust field names as per Apply model

            # Save data to the ItemPurchased model
            ItemPurchased.objects.create(
                apply=apply_instance,
                date=date,
                item_name=item_name,
                price=price,
                bill_photo=bill_photo,
                customer_name=customer_name,  # Include customer_name
                issue=issue  # Include issue
            )
            messages.success(request, "Item purchased successfully added!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('itempurchased', apply_id=apply_id)

        return redirect('itempurchased', apply_id=apply_id)

    # Fetch all item purchases for this Apply instance
    items = ItemPurchased.objects.filter(apply=apply_instance)
    context = {
        'apply': apply_instance,
        'items': items
    }
    return render(request, 'itempurchased.html', context)

def updateitempurchased(request, item_id):
    # Get the item or return a 404 if not found
    item = get_object_or_404(ItemPurchased, id=item_id)
    
    if request.method == "POST":
        # Retrieve data from the form
        date = request.POST.get('date')
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        bill_photo = request.FILES.get('bill_photo')  # Handle file upload
        
        # Validate required fields
        if not all([date, item_name, price]):
            messages.error(request, "All fields except bill photo are required.")
            return render(request, 'updateitempurchased.html', {'item': item})

        try:
            # Update the item fields
            item.date = date
            item.item_name = item_name
            item.price = price

            # Update the bill photo only if a new one is uploaded
            if bill_photo:
                item.bill_photo = bill_photo

            item.save()
            messages.success(request, "Item purchased updated successfully!")
            return redirect('itempurchased', apply_id=item.apply.id)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'updateitempurchased.html', {'item': item})

    # Pass the item instance to the template
    return render(request, 'updateitempurchased.html', {'item': item}) 





def vendorinfo(request, apply_id):
    apply_instance = get_object_or_404(Apply, id=apply_id)

    if request.method == "POST":
        # Retrieve form data
        date = request.POST.get('date')
        vendor_name = request.POST.get('vendor_name')
        vendor_bill_photo = request.FILES.get('vendor_bill_photo')
        vendor_eta = request.POST.get('vendor_eta')
        vendor_cost = request.POST.get('vendor_cost')

        # Validate required fields
        if not all([date, vendor_name, vendor_bill_photo, vendor_eta, vendor_cost]):
            messages.error(request, "All fields are required.")
            return redirect('vendorinfo', apply_id=apply_id)

        try:
            # Fetch customer_name and issue from Apply instance
            customer_name = apply_instance.name  # Adjust based on Apply model
            issue = apply_instance.issue  # Adjust based on Apply model

            # Save data to the VendorInfo model
            VendorInfo.objects.create(
                apply=apply_instance,
                date=date,
                vendor_name=vendor_name,
                vendor_bill_photo=vendor_bill_photo,
                vendor_eta=vendor_eta,
                vendor_cost=vendor_cost,
                customer_name=customer_name,  # Store customer_name
                issue=issue  # Store issue
            )
            messages.success(request, "Vendor info successfully added!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('vendorinfo', apply_id=apply_id)

        return redirect('vendorinfo', apply_id=apply_id)

    # Fetch all VendorInfo records for the current Apply instance
    vendors = VendorInfo.objects.filter(apply=apply_instance)
    context = {
        'apply': apply_instance,
        'vendors': vendors,
    }
    return render(request, 'vendorinfo.html', context)



def updatevendorinfo(request, vendor_id):
    # Get the vendor info instance or return a 404 if not found
    vendor = get_object_or_404(VendorInfo, id=vendor_id)
    
    if request.method == "POST":
        # Retrieve data from the form
        date = request.POST.get('date')
        vendor_name = request.POST.get('vendor_name')
        vendor_eta = request.POST.get('vendor_eta')
        vendor_cost = request.POST.get('vendor_cost')
        vendor_bill_photo = request.FILES.get('vendor_bill_photo')  # Handle file upload

        # Validate required fields
        if not all([date, vendor_name, vendor_eta, vendor_cost]):
            messages.error(request, "All fields except vendor bill photo are required.")
            return render(request, 'updatevendorinfo.html', {'vendor': vendor})

        try:
            # Update the vendor fields
            vendor.date = date
            vendor.vendor_name = vendor_name
            vendor.vendor_eta = vendor_eta
            vendor.vendor_cost = vendor_cost

            # Update the bill photo only if a new one is uploaded
            if vendor_bill_photo:
                vendor.vendor_bill_photo = vendor_bill_photo

            vendor.save()
            messages.success(request, "Vendor info updated successfully!")
            return redirect('vendorinfo', apply_id=vendor.apply.id)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'updatevendorinfo.html', {'vendor': vendor})

    # Pass the vendor instance to the template
    return render(request, 'updatevendorinfo.html', {'vendor': vendor})




def currentstatus(request, apply_id):
    apply_instance = get_object_or_404(Apply, id=apply_id)

    if request.method == "POST":
        # Retrieve form data
        date = request.POST.get('date')
        technician_name = request.POST.get('technician_name')
        status = request.POST.get('status')

        # Validate required fields
        if not all([date, technician_name, status]):
            messages.error(request, "All fields are required.")
            return redirect('currentstatus', apply_id=apply_id)

        try:
            # Fetch customer_name and issue from Apply instance
            customer_name = apply_instance.name  # Adjust based on your Apply model
            issue = apply_instance.issue  # Adjust based on your Apply model

            # Save data to the CurrentStatus model
            CurrentStatus.objects.create(
                apply=apply_instance,
                date=date,
                technician_name=technician_name,
                status=status,
                customer_name=customer_name,  # Store customer_name
                issue=issue  # Store issue
            )
            messages.success(request, "Current status successfully added!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('currentstatus', apply_id=apply_id)

        return redirect('currentstatus', apply_id=apply_id)

    # Fetch all CurrentStatus records for this Apply instance
    status = CurrentStatus.objects.filter(apply=apply_instance)
    context = {
        'apply': apply_instance,
        'status': status,
    }
    return render(request, 'currentstatus.html', context)

def updatecurrentstatus(request, status_id):
    status = get_object_or_404(CurrentStatus, id=status_id)

    if request.method == "POST":
        status.date = request.POST.get('date')
        status.technician_name = request.POST.get('technician_name')
        status.status = request.POST.get('status')
        status.save()

        return redirect('currentstatus', apply_id=status.apply.id)

    return render(request, 'updatecurrentstatus.html', {'status': status})












        








