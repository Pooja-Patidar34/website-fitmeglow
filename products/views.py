# products/views.py
import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product, Wishlist, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def product_list(request):
    products = Product.objects.all().order_by('name')

    # Handle filtering based on checkboxes
    product_types = request.GET.getlist('product_types')
    skin_concerns = request.GET.getlist('skin_concerns')
    skin_types = request.GET.getlist('skin_types')

    filter_query = Q()
    if product_types:
        filter_query &= Q(product_types__name__in=product_types)
    if skin_concerns:
        filter_query &= Q(skin_concerns__name__in=skin_concerns)
    if skin_types:
        filter_query &= Q(skin_types__name__in=skin_types)
    
    if filter_query:
        products = products.filter(filter_query).distinct()

    # Handle sorting by price
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # AJAX handling for product list partial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('products/product_list_partial.html', {'products': products})
        return JsonResponse({'html': html})

    # Context for rendering the full page
    context = {
        'products': products,
        'selected_product_types': product_types,
        'selected_skin_concerns': skin_concerns,
        'selected_skin_types': skin_types,
        'sort_by': sort_by,
    }

    return render(request, 'home.html', context)

def homepage(request):
    products = Product.objects.all().order_by('name')

    # Handle filtering based on checkboxes
    product_types = request.GET.getlist('product_types')
    skin_concerns = request.GET.getlist('skin_concerns')
    skin_types = request.GET.getlist('skin_types')

    if product_types:
        products = products.filter(product_types__name__in=product_types).distinct()
    if skin_concerns:
        products = products.filter(skin_concerns__name__in=skin_concerns).distinct()
    if skin_types:
        products = products.filter(skin_types__name__in=skin_types).distinct()

    # Handle sorting by price
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # AJAX handling for product list partial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('products/product_list_partial.html', {'products': products})
        return JsonResponse({'html': html})

    # Context for rendering the full page
    context = {
        'products': products,
        'selected_product_types': product_types,
        'selected_skin_concerns': skin_concerns,
        'selected_skin_types': skin_types,
        'sort_by': sort_by,
    }

    return render(request, 'home.html', context)
    
def contact_us(request):
    return render(request, 'contact.html')

@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'wishlist': user.wishlist_set.all(),
        'cart': user.cart_set.all(),
    }
    return render(request, 'account/dashboard.html', context)



def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

@login_required
def wishlist_view(request):
    try:
        wishlist = request.user.wishlist
        products = wishlist.products.all()
    except Wishlist.DoesNotExist:
        wishlist = None
        products = []

    return render(request, 'products/wishlist.html', {'products': products})

@login_required
def add_to_wishlist_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if not product.is_in_stock:
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect('product_list')  

    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f'{product.name} has been added to your wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    
    return redirect('wishlist')

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not product.is_in_stock:
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect('product_detail', product_id=product_id)

    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        # If item is newly added to cart, set its quantity and price
        cart_item.quantity = quantity
        cart_item.price = product.current_price
    else:
        # If item already exists in cart, update its quantity and ensure price is updated
        cart_item.quantity += quantity
        if cart_item.price is None:  # Ensure price is set if it was None
            cart_item.price = product.current_price

    # Save the cart item with updated quantity and price
    cart_item.save()

    messages.success(request, f'{product.name} (Quantity: {quantity}) has been added to your cart.')
    return redirect('cart')


@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum((item.price if item.price is not None else item.product.current_price) * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'products/cart.html', context)



@login_required
def remove_from_cart_view(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.delete()
    product_name = cart_item.product.name  # Get the name of the product being removed
    messages.success(request, f'{product_name} has been removed from your cart.')
    return redirect('cart')

@login_required
def add_selected_to_cart_view(request):
    if request.method == 'POST':
        selected_product_ids = request.POST.getlist('selected_products')
        
        if not selected_product_ids:
            messages.warning(request, "No items selected.")
            return redirect('wishlist')
        
        products = Product.objects.filter(id__in=selected_product_ids)
        cart, created = Cart.objects.get_or_create(user=request.user)

        added_products = []
        for product in products:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            added_products.append(product.name)

        if added_products:
            messages.success(request, f"Added {', '.join(added_products)} to your cart.")

        return redirect('wishlist')  # Redirect to wishlist or cart page after adding to cart
    else:
        return redirect('wishlist') # Redirect to wishlist or appropriate page if not POST

@login_required
def add_all_to_cart_view(request):
    if request.method == 'POST':
        wishlist = Wishlist.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(user=request.user)

        added_products = []
        for product in wishlist.products.all():
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            added_products.append(product.name)

        if added_products:
            messages.success(request, f"Added {', '.join(added_products)} to your cart.")

        return redirect('wishlist')  # Redirect to wishlist or cart page after adding to cart
    else:
        return redirect('wishlist')
        
@login_required
def remove_from_wishlist(request, product_id):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f'{product.name} has been removed from your wishlist.')
    else:
        messages.error(request, f'{product.name} was not found in your wishlist.')
    
    return redirect('wishlist')

def update_cart_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity'))
        product_name = item.product.name  # Get the product name

        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, f'{product_name} updated successfully.')
        else:
            item.delete()
            messages.success(request, f'{product_name} removed successfully.')

    return redirect('cart') 

# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.current_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        print("POST request received")
        print("Total price:", total_price)
        print("Stripe token:", request.POST.get('stripeToken'))

        try:
            charge = stripe.Charge.create(
                amount=int(total_price * 100),
                currency='usd',
                source=request.POST['stripeToken'],
                description='Order charge'
            )
            print("Charge created:", charge)
            
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                status='Paid'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.current_price
                )

            cart_items.delete()
            return redirect('order_success')

        except stripe.error.CardError as e:
            messages.error(request, f'Card error: {e.error.message}')
            print(f'CardError: {e.error.message}')

        except stripe.error.InvalidRequestError as e:
            messages.error(request, 'Invalid parameters for payment.')
            print('InvalidRequestError:', e)

        except stripe.error.AuthenticationError as e:
            messages.error(request, 'Authentication with payment gateway failed.')
            print('AuthenticationError:', e)

        except stripe.error.APIConnectionError as e:
            messages.error(request, 'Network error with payment gateway.')
            print('APIConnectionError:', e)

        except stripe.error.StripeError as e:
            messages.error(request, 'Payment gateway error. Please try again later.')
            print('StripeError:', e)

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            print('Exception:', e)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'products/checkout.html', context)

@login_required
def order_success(request):
    # Retrieve the latest order for the user
    order = Order.objects.filter(user=request.user).latest('created_at')
    context = {
        'order': order
    }
    return render(request, 'products/order_success.html', context)

