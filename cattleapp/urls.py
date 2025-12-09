from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='home'),# ' ' -> maps directly to http://127.0.0.1 
    path('ajax-signup/', views.ajax_signup, name='ajax_signup'),
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    path('adminpanel/', views.adminpanel_view, name='adminpanel'),
    path('userpanel/', views.userpanel_view, name='userpanel'),
    path("view_cow/", views.view_cow, name="view_cow"),
    path("add_cow/", views.add_cow, name="add_cow"),
    path('fetch-cows/', views.fetch_cows, name='fetch_cows'),
    path("view_cow/get-cow/<str:tag_id>/", views.get_cow, name="get_cow"),
    path("view_cow/update-cow/<str:tag_id>/", views.update_cow, name="update_cow"),
    path("view_cow/delete-cow/<str:tag_id>/", views.delete_cow, name="delete_cow"),
     # STAFF CRUD
    path("staff/register/", views.staff_register_page, name="staff_register_page"),
    path("staff/add/", views.add_staff_ajax, name="add_staff_ajax"),
    path("staff/fetch/", views.fetch_staff, name="fetch_staff"),
    path("staff/get/<int:id>/", views.get_staff, name="get_staff"),
    path("staff/update/<int:id>/", views.update_staff, name="update_staff"),
    path("staff/delete/<int:id>/", views.delete_staff, name="delete_staff"),
    # ============================
    # TASK ROUTES
    # ============================
    path("tasks/", views.task_page, name="task_page"),
    path("tasks/fetch/", views.fetch_tasks, name="fetch_tasks"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/get/<int:id>/", views.get_task, name="get_task"),
    path("tasks/update/<int:id>/", views.update_task, name="update_task"),
    path("tasks/delete/<int:id>/", views.delete_task, name="delete_task"),

    # ============================
    # ATTENDANCE ROUTES
    # ============================
    path("attendance/", views.attendance_page, name="attendance_page"),
    path("attendance/fetch/", views.fetch_attendance, name="fetch_attendance"),
    path("attendance/add/", views.add_attendance, name="add_attendance"),
    path("attendance/get/<int:id>/", views.get_attendance, name="get_attendance"),
    path("attendance/update/<int:id>/", views.update_attendance, name="update_attendance"),
    path("attendance/delete/<int:id>/", views.delete_attendance, name="delete_attendance"),

    # ============================
    # PERFORMANCE ROUTES
    # ============================
    path("performance/", views.performance_page, name="performance_page"),
    path("performance/fetch/", views.fetch_performance, name="fetch_performance"),
    path("performance/add/", views.add_performance, name="add_performance"),
    path("performance/get/<int:id>/", views.get_performance, name="get_performance"),
    path("performance/update/<int:id>/", views.update_performance, name="update_performance"),
    path("performance/delete/<int:id>/", views.delete_performance, name="delete_performance"),
    
     # Milk Production URLs
    path("milk/production/", views.milk_production_page, name="milk_production_page"),
    path("milk/production/add/", views.add_milk_production_ajax, name="add_milk_production_ajax"),
    path("milk/production/fetch/", views.fetch_milk_production, name="fetch_milk_production"),
    path("milk/production/get/<int:id>/", views.get_milk_production, name="get_milk_production"),
    path("milk/production/update/<int:id>/", views.update_milk_production, name="update_milk_production"),
    path("milk/production/delete/<int:id>/", views.delete_milk_production, name="delete_milk_production"),

    # Milk Sales
    path("milk/sales/", views.milk_sales_page, name="milk_sales_page"),
    path("milk/sales/add/", views.add_milk_sale_ajax, name="add_milk_sale_ajax"),
    path("milk/sales/fetch/", views.fetch_milk_sales, name="fetch_milk_sales"),
    path("milk/sales/get/<int:id>/", views.get_milk_sale, name="get_milk_sale"),
    path("milk/sales/update/<int:id>/", views.update_milk_sale, name="update_milk_sale"),
    path("milk/sales/delete/<int:id>/", views.delete_milk_sale, name="delete_milk_sale"),
    
     # Milk Buyer URLs 
    path("milk/buyers/", views.milk_buyer_page, name="milk_buyer_page"),
    path("milk/buyers/add/", views.add_milk_buyer_ajax, name="add_milk_buyer_ajax"),
    path("milk/buyers/fetch/", views.fetch_milk_buyers, name="fetch_milk_buyers"),
    path("milk/buyers/get/<int:id>/", views.get_milk_buyer, name="get_milk_buyer"),
    path("milk/buyers/update/<int:id>/", views.update_milk_buyer, name="update_milk_buyer"),
    path("milk/buyers/delete/<int:id>/", views.delete_milk_buyer, name="delete_milk_buyer"),
    

    # ============================
    # Health & Veterinary URLs
    # ============================
    # Vaccination Scheduler
    path("health/vaccinations/", views.vaccination_scheduler_page, name="vaccination_scheduler"),
    path("health/vaccinations/add/", views.add_vaccination_ajax, name="add_vaccination_ajax"),
    path("health/vaccinations/fetch/", views.fetch_vaccinations, name="fetch_vaccinations"),
    path("health/vaccinations/get/<int:id>/", views.get_vaccination, name="get_vaccination"),
    path("health/vaccinations/update/<int:id>/", views.update_vaccination, name="update_vaccination"),
    path("health/vaccinations/delete/<int:id>/", views.delete_vaccination, name="delete_vaccination"),

    # Deworming Reminders
    path("health/deworming/", views.deworming_reminders_page, name="deworming_reminders"),
    path("health/deworming/add/", views.add_deworming_ajax, name="add_deworming_ajax"),
    path("health/deworming/fetch/", views.fetch_deworming, name="fetch_deworming"),
    path("health/deworming/get/<int:id>/", views.get_deworming, name="get_deworming"),
    path("health/deworming/update/<int:id>/", views.update_deworming, name="update_deworming"),
    path("health/deworming/delete/<int:id>/", views.delete_deworming, name="delete_deworming"),

    # Disease Monitoring
    path("health/diseases/", views.disease_monitoring_page, name="disease_monitoring"),
    path("health/diseases/add/", views.add_disease_ajax, name="add_disease_ajax"),
    path("health/diseases/fetch/", views.fetch_diseases, name="fetch_diseases"),
    path("health/diseases/get/<int:id>/", views.get_disease, name="get_disease"),
    path("health/diseases/update/<int:id>/", views.update_disease, name="update_disease"),
    path("health/diseases/delete/<int:id>/", views.delete_disease, name="delete_disease"),

    # Treatment History
    path("health/treatments/", views.treatment_history_page, name="treatment_history"),
    path("health/treatments/add/", views.add_treatment_ajax, name="add_treatment_ajax"),
    path("health/treatments/fetch/", views.fetch_treatments, name="fetch_treatments"),
    path("health/treatments/get/<int:id>/", views.get_treatment, name="get_treatment"),
    path("health/treatments/update/<int:id>/", views.update_treatment, name="update_treatment"),
    path("health/treatments/delete/<int:id>/", views.delete_treatment, name="delete_treatment"),
     

    # ============================
    # FEED & NUTRITION URLs
    # ============================

    # A. Feed Inventory
    path("feed/inventory/", views.feed_inventory_page, name="feed_inventory_page"),
    path("feed/inventory/add/", views.add_feed_ajax, name="add_feed_ajax"),
    path("feed/inventory/fetch/", views.fetch_feeds, name="fetch_feeds"),
    path("feed/inventory/get/<int:id>/", views.get_feed, name="get_feed"),
    path("feed/inventory/update/<int:id>/", views.update_feed, name="update_feed"),
    path("feed/inventory/delete/<int:id>/", views.delete_feed, name="delete_feed"),

    # B. Daily Feeding Plans
    path("feed/plans/", views.feeding_plan_page, name="feeding_plan_page"),
    path("feed/plans/add/", views.add_feeding_plan_ajax, name="add_feeding_plan_ajax"),
    path("feed/plans/fetch/", views.fetch_feeding_plans, name="fetch_feeding_plans"),
    path("feed/plans/get/<int:id>/", views.get_feeding_plan, name="get_feeding_plan"),
    path("feed/plans/update/<int:id>/", views.update_feeding_plan, name="update_feeding_plan"),
    path("feed/plans/delete/<int:id>/", views.delete_feeding_plan, name="delete_feeding_plan"),

    # C. Feed Cost Tracking / Purchases
    path("feed/purchases/", views.feed_purchase_page, name="feed_purchase_page"),
    path("feed/purchases/add/", views.add_feed_purchase_ajax, name="add_feed_purchase_ajax"),
    path("feed/purchases/fetch/", views.fetch_feed_purchases, name="fetch_feed_purchases"),
    path("feed/purchases/get/<int:id>/", views.get_feed_purchase, name="get_feed_purchase"),
    path("feed/purchases/update/<int:id>/", views.update_feed_purchase, name="update_feed_purchase"),
    path("feed/purchases/delete/<int:id>/", views.delete_feed_purchase, name="delete_feed_purchase"),
 


    path('logout/', views.logout_view, name='logout'),
    #path('logout/', views.logout_view, name='logout'),
    #path('maindashboard/', views.maindashboard, name='maindashboard'),
]
