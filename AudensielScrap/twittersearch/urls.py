# twittersearch/urls.py
from django.urls import path
from . import views

urlpatterns = [
            #exemple: http://localhost:8000/api/search/taylor/2020-12-02/2018-08-16/20
            path('search/<str:mot_cle>/<str:until_date>/<str:since_date>/<int:nb_tweets>', views.get_tweets, name='search'),
            #exemple:http://localhost:8000/api/display_new/202401022358
            path('display_new/<str:req_id>',views.get_tweet_by_reqid,name="display_new"),
            #exemple: http://localhost:8000/api/display_all
            path('display_all',views.get_all_tweet, name = "display_all_tweet"),
            path('display_req',views.get_all_req, name = "display_all_req")
        ]
            
