"""Exact GELU via the normal CDF; analytical derivatives. Run with Python + NumPy + SciPy + Matplotlib."""
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/dl-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expit, ndtr
from pathlib import Path
OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.size':12, 'axes.spines.top':False, 'axes.spines.right':False, 'figure.facecolor':'#fafaf7', 'axes.facecolor':'#fafaf7'})
COLORS=['#2563eb','#d97706','#15803d']
NAMES=['ReLU','SiLU','GELU (exact)']
def vals(x):return [np.maximum(0,x),x*expit(x),x*ndtr(x)]
def style(ax,title,ylabel):
    ax.set_title(title,pad=16,fontsize=16,fontweight='bold')
    ax.axhline(0,color='#64748b',lw=.8);ax.axvline(0,color='#64748b',lw=.8)
    ax.set_xlabel('Input x');ax.set_ylabel(ylabel);ax.grid(alpha=.16)
    ax.legend(frameon=False,loc='upper left')
def save(fig,name):
    fig.savefig((OUT/name).with_suffix('.svg'),bbox_inches='tight');plt.close(fig)
x=np.linspace(-4,4,1601)
fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
for y,c,n,ls in zip(vals(x),COLORS,NAMES,['-','--','-.']):ax.plot(x,y,color=c,label=n,lw=2.5,ls=ls)
style(ax,'1. Forward outputs: same input, different responses','Output f(x)')
ax.set_xlim(-4,4);ax.set_ylim(-.6,4.15)
save(fig,'01-outputs.png')
x=np.linspace(-3,1.5,1201)
fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
for y,c,n,ls in zip(vals(x),COLORS,NAMES,['-','--','-.']):ax.plot(x,y,color=c,label=n,lw=2.5,ls=ls)
for y,c in zip(vals(np.array([-2.])),COLORS):ax.scatter([-2],y,color=c,s=45,zorder=5)
ax.text(-2.85,.8,'At x = -2:\nReLU = 0\nSiLU = -0.238\nGELU = -0.046',bbox=dict(facecolor='white',edgecolor='#d1d5db',boxstyle='round,pad=.6'))
style(ax,'2. Zoom: negative inputs are not all cut to zero','Output f(x)')
ax.set_xlim(-3,1.5);ax.set_ylim(-.4,1.5);ax.legend(loc='upper right',frameon=False)
save(fig,'02-negative-zoom.png')
x=np.linspace(-4,4,1601);s=expit(x)
derivs=[s+x*s*(1-s),ndtr(x)+x*np.exp(-x*x/2)/np.sqrt(2*np.pi)]
fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
ax.plot([-4,0],[0,0],color=COLORS[0],lw=2.5,label='ReLU')
ax.plot([0,4],[1,1],color=COLORS[0],lw=2.5)
ax.scatter([0,0],[0,1],s=55,facecolors='#fafaf7',edgecolors=COLORS[0],zorder=6)
for y,c,n,ls in zip(derivs,COLORS[1:],NAMES[1:],['--','-.']):ax.plot(x,y,color=c,label=n,lw=2.5,ls=ls)
ax.scatter([0],[.5],color='#111827',zorder=7,s=45)
ax.annotate('SiLU\'(0) = GELU\'(0) = 0.5',xy=(0,.5),xytext=(-3.6,.75),arrowprops=dict(arrowstyle='->',color='#334155'))
style(ax,'3. Derivatives: multiply the upstream gradient by this value',"Local derivative f'(x)")
ax.set_xlim(-4,4);ax.set_ylim(-.23,1.35)
fig.text(.5,-.025,'ReLU derivative is undefined at 0 mathematically; open circles show the one-sided limits.',ha='center',fontsize=10,color='#475569')
save(fig,'03-derivatives.png')
# Verify derivatives against central differences away from the ReLU corner.
t=np.linspace(-3.9,3.9,301);h=1e-5
for i in [1,2]:
    numerical=(vals(t+h)[i]-vals(t-h)[i])/(2*h)
    sig=expit(t)
    analytical=sig+t*sig*(1-sig) if i==1 else ndtr(t)+t*np.exp(-t*t/2)/np.sqrt(2*np.pi)
    np.testing.assert_allclose(numerical,analytical,atol=1e-8,rtol=1e-6)
assert np.allclose([vals(np.array([0.]))[i][0] for i in range(3)],0)
print('Created 3 figures; analytical derivatives verified against finite differences.')
