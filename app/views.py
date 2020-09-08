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

# グラフ表示用
import matplotlib
import matplotlib.pyplot as plt
import io


@login_required
def homeview(request):
    YEAR = datetime.datetime.now().strftime("%Y")
    MONTH= datetime.datetime.now().strftime("%B")
    object_list = request.user.healthapp_set.all().order_by('postdate')
    context = {
        'year':YEAR,
        'month':MONTH,
        'object_list':object_list, 
        'Input':InputForm(),
        }

    return render(request, 'app/home.html', context)

def create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        helathapp = form.save(commit=True)
        helathapp.user = request.user
        helathapp.save()
    return HttpResponseRedirect(reverse('home'))

def delete(request, id=None):
    post = get_object_or_404(HealthApp, pk=id)
    post.delete()
    return HttpResponseRedirect(reverse('home'))


# グラフ表示用
#バックエンドを指定
matplotlib.use('Agg')

#グラフ作成
def setPlt():
    lists = HealthApp.objects.all().order_by('postdate')
    weight = [float(data.weight) for data in lists]
    steps = [int(data.steps) for data in lists]
    postdates = [str(data.postdate) for data in lists]

    date = []
    for dates in sorted(postdates):
        day = str(dates.split("-")[2])
        #month = str(dates.split("-")[1])
        #postdate = month + "/" + day
        #date.append(postdate)
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
    setPlt()  
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response






