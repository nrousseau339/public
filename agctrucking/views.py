from http.client import HTTPSConnection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connections
from urllib3 import HTTPResponse
from .models import *
from .forms import *
from datetime import datetime

# Create your views here.


def main(request):
    update_query = """insert into order_data select ordernumber, custnmbr, shipdate, 
                        internalproductname, tons, shipdate, PromiseDate,0, 
                        null, null, 0 from amgil..Z_TruckLog
                        where status = 'openorder' 
                        and ordernumber not in (select sopnumbe from order_data);
                        update order_data set sopnumbe = rtrim(sopnumbe);
                        update order_data
                        set projectedshipdate = b.shipdate, 
                        RequestedDeliveryDate = b.PromiseDate
                        from order_data a inner join (select ordernumber, shipdate, PromiseDate from amgil..Z_TruckLog) b on a.sopnumbe = b.ordernumber
                    """

    with connections["agc"].cursor() as cursor:
        cursor.execute(update_query)
        print("Order data has been updated.")

    orders = (
        order_data.objects.filter(shipped=False)
        .values_list(
            "sopnumbe",
            "cstnmbr",
            "originalshipdate",
            "product",
            "tons",
            "projectedshipdate",
            "requesteddeliverydate",
            "truckingconfirmed",
            "shippingcontact",
            "correspondencenotes",
            "shipped",
        )
        .order_by("projectedshipdate")
    )

    context = {
        "orders": orders,
    }

    return render(request, "agctrucking/list.html", context)


def shipped(request):

    orders = order_data.objects.filter(shipped=True).values_list(
        "sopnumbe",
        "cstnmbr",
        "originalshipdate",
        "product",
        "tons",
        "projectedshipdate",
        "requesteddeliverydate",
        "truckingconfirmed",
        "shippingcontact",
        "correspondencenotes",
        "shipped",
    )

    context = {
        "orders": orders,
    }

    return render(request, "agctrucking/list.html", context)


def edit(request, ord):
    try:
        order = order_data.objects.get(sopnumbe=ord)
        form = AgcTruckingForm(instance=order)
        query = (
            # """select OrderNumber, ShipDate, PromiseDate from amgil..x_spaceshuttle where ordernumber = '"""
            """select sopnumbe, projectedshipdate, requesteddeliverydate from order_data where sopnumbe = '"""
            + ord
            + "'"
        )
        try:
            with connections["agc"].cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()

            gpshipdate = row[1]
            gpreqdeldate = row[2]
            gpstring = "The ship date in GP is "
            gpstring1 = ". The requested delivery date in GP is "
        except:
            message = "There was an error. Error 1."
            context = {"message": message}
            return render(request, "agctrucking/error.html", context)

        if request.method == "POST":
            form = AgcTruckingForm(request.POST, instance=order)
            if form.is_valid():
                try:
                    form.save()
                    # this will be an update query to update the dates in GP when button form is submitted.
                    query_update1 = """update amgil..x_ext_salesdata 
                                        set PromiseDate = (select RequestedDeliveryDate from order_data where sopnumbe = '%s')
                                        where SOPNumber = '%s'""" % (
                        ord,
                        ord,
                    )
                    query_update2 = """update amgil..x_ext_salesdata 
                                        set ShippingDate = (select ProjectedShipDate from order_data where sopnumbe = '%s')
                                        where SOPNumber = '%s'""" % (
                        ord,
                        ord,
                    )

                    with connections["agc"].cursor() as cursor:
                        cursor.execute(query_update1)
                        cursor.execute(query_update2)
                        # message = query_update
                        message = "Data updated successfully!"
                        context = {"message": message}
                        return render(request, "agctrucking/update.html", context)
                except:
                    message = "There was an error. Error 2."
                    context = {"message": message}
                    return render(request, "agctrucking/error.html", context)
                # return redirect("agctrucking:update")
    except:
        message = "There was an error with the request. Error 3."
        context = {"message": message}
        return render(request, "agctrucking/error.html", context)

    context = {
        "order": order,
        "form": form,
        "gpstring": gpstring,
        "gpstring1": gpstring1,
        "gpshipdate": gpshipdate,
        "gpreqdeldate": gpreqdeldate,  # promisedate or ETA or whatever
    }

    return render(request, "agctrucking/edit.html", context)


def delete_order(request, ord):
    order = order_data.objects.get(sopnumbe=ord)
    form = AgcTruckingForm(instance=order)
    query = (
        # """select OrderNumber, ShipDate, PromiseDate from amgil..x_spaceshuttle where ordernumber = '"""
        """select sopnumbe, projectedshipdate, requesteddeliverydate from order_data where sopnumbe = '"""
        + ord
        + "'"
    )

    if request.method == "POST":
        order.delete()
        return redirect("agctrucking:main")

    context = {
        "order": order,
    }
    return render(request, "agctrucking/delete.html", context)
