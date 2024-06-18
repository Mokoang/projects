# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.db import connection
# from datetime import  date
# from .models import lease,lease_details


# @receiver(user_logged_in)
# def user_logged_in_handler(sender, request, user, **kwargs):
    # # Your logic after user logs in
    # for lease_data in lease.objects.filter(lease_status='A'):
        # latest_details = lease_details.objects.filter(lease_number=lease_data).order_by('-id').first()

        # if latest_details and latest_details.period != date.today().year:
            # RegisteredLeaseDetails.objects.create(
                # lease_number=lease_data,
                # period=date.today().year,
                # zone_number=latest_details.zone_number,
                # area=latest_details.area,
                # area_units=latest_details.area_units,
                # landuse_type=latest_details.landuse_type,
                # fixed_rate=latest_details.fixed_rate,
                # penalty=latest_details.penalty
            # )

    # # Add your custom logic here
