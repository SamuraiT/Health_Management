from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from .models import HealthApp
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import datetime
from .forms import PostForm, InputForm
from dateutil.relativedelta import relativedelta

# グラフ表示用
import matplotlib
import matplotlib.pyplot as plt
import io


today = datetime.datetime.now()
year = today.strftime("%Y")
month = today.strftime("%B")         #英語表記         
current_month = today.strftime("%m") #数字表記


def get_next(year, month):
    year = int(year)
    month = int(month)
    if month == "Jan":
        return int(year) +1, month
    else:
        return year, int(month) +1


def get_prev(year, month):
    year = int(year)
    month = int(month)
    if month == "Jan":
        return int(year) -1, month
    else:
        return year, int(month) -1 


@login_required
def homeview(request, year, month):
    next_year, next_month = get_next(year, month)
    prev_year, prev_month = get_prev(year, month)
    object_list = request.user.healthapp_set.all().order_by('postdate').filter(
        postdate__month = month,
        postdate__year = year)
    context = {
        'year':year,
        'month':month,
        'next_month':next_month,
        'next_year':next_year,
        'prev_month':prev_month,
        'prev_year':prev_year,
        'object_list':object_list, 
        'Input':InputForm(),
        }

    return render(request, 'app/home.html', context)

def create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        healthapp = form.save(commit=True)
        healthapp.user = request.user
        healthapp.save()
    return HttpResponseRedirect(reverse('home'))

def delete(request, id=None):
    post = get_object_or_404(HealthApp, pk=id)
    post.delete()
    return HttpResponseRedirect(reverse('home'))


# グラフ表示用
#バックエンドを指定
matplotlib.use('Agg')

#グラフ作成
def setPlt(request):
#    lists = request.user.healthapp_set.all().order_by('postdate').filter(postdate__month = current_month)
    lists = request.user.healthapp_set.all().order_by('postdate').filter(postdate__month = month)
    weight = [float(data.weight) for data in lists]
    steps = [int(data.steps) for data in lists]
    postdates = [str(data.postdate) for data in lists]

    date = []
    for dates in sorted(postdates):
        day = str(dates.split("-")[2])
        date.append(day)
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(date, weight, linewidth=2, color="red", linestyle="solid", marker="o", markersize=8)
    ax2.bar(date, steps, width=0.4)

    #折れ線グラフを前面
    ax1.set_zorder(2)
    ax2.set_zorder(1)

    #折れ線グラフの背景を透明
    ax1.patch.set_alpha(0)

    #グリッド表示(ax1のみ)
    ax1.grid(True)

    #軸ラベルを表示
    plt.xlabel('Date')
    ax1.set_ylabel('Weight')
    ax2.set_ylabel('Steps')

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

# 実行するビュー関数
def get_svg(request):
    setPlt(request)  
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response




