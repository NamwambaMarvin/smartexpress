
###############################
##### ADD FUNCTIONS ###########
###############################
def add_product(request, product_slug):
    context = {
        "form" : addproduct(),
    }
    return render(request, "admin_templates/add_product", context=context)

def add_category(request, category_slug):
    context = {
        "form" : addcategory(),
    }
    return render(request, "admin_templates/add_category", context=context)

def add_shop(request, shop_slug):
    context = {
        "form" : addshop(),
    }
    return render(request, "admin_templates/add_shop", context=context)

def add_subcategory(request, sub_category_slug):
    context = {
        "form" : addsubcategory(),
    }
    return render(request, "admin_templates/add_subcategory", context=context)

def add_category_front_page(request, category_slug):
    context = {
        "form" : addcategory_front_page(),
    }
    return render(request, "admin_templates/add_category_banner", context=context)

def add_brand(request, brand_id):
    context = {
        "form" : addbrand(),
    }
    return render(request, "admin_templates/add_brand", context=context)

###############################
##### DELETE FUNCTIONS ###########
###############################
def delete_product(request, product_slug):
    # Get products categoty and store it
    # Delete the product
    # Redirect the user to products of
    # that category
    return redirect("/products")

def delete_category(request, category_slug):
    return redirect(f"/products/{category_slug}")

def delete_shop(request, shop_slug):
    return redirect("/")

def delete_subcategory(request, sub_category_slug):
    return redirect("/subproducts/category_name/sub_cat_name")

def delete_category_front_page(request, category_slug):
    return redirect(f"/products/{category_slug}")

def delete_brand(request, brand_id):
    return redirect("/")