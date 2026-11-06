#!/usr/bin/env python3
"""Atölye header. Requires Pillow. Use --font and --bold for other systems."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--font',default='/System/Library/Fonts/Supplemental/Arial.ttf')
p.add_argument('--bold',default='/System/Library/Fonts/Supplemental/Arial Bold.ttf')
a=p.parse_args()
S=2
for mode,bg,ink,muted,accent,border in [('light','#f3f4f4','#242729','#555d63','#b52b32','#d9dddf'),('dark','#1b1e22','#f0f1f2','#b1b8bf','#f0777e','#3b424a')]:
 im=Image.new('RGB',(1200*S,480*S),bg);d=ImageDraw.Draw(im)
 def text(x,y,s,size=24,c=ink,b=False):d.text((x*S,y*S),s,font=ImageFont.truetype(a.bold if b else a.font,size*S),fill=c)
 def rr(box,c,r=0,outline=None):d.rounded_rectangle(tuple(int(v*S) for v in box),r*S,fill=c,outline=outline,width=S)
 text(48,48,'Hüseyin Durna',52,b=True)
 text(48,144,'İşte ihtiyaç duyduğum',34)
 text(48,188,'araçları yazıyorum',34)
 rr((48,276,100,280),accent)
 text(48,316,'Bir sipariş ekranı.',24,muted)
 text(48,352,'Görev çubuğunda küçük bir gösterge.',24,muted)
 # Real Lumen screenshot; crop to the header and order rows, using demo data.
 src=Image.open(ROOT/'tools/atelier/lumen-demo.png').convert('RGB').crop((24,64,1400,504))
 src=src.resize((496*S,159*S),Image.Resampling.LANCZOS)
 rr((648,48,1152,284),'#ffffff',8,border)
 d.rounded_rectangle((648*S,48*S,1152*S,100*S),8*S,fill='#ffffff')
 text(664,62,'Lumen',22,'#242729',True);text(1032,66,'Demo',16,'#626b73')
 im.paste(src,(652*S,108*S))
 text(648,310,'Windows Stats',21,muted)
 src=Image.open(ROOT/'tools/atelier/windows-stats.png').convert('RGB')
 w=504*S;h=round(src.height*w/src.width);src=src.resize((w,h),Image.Resampling.NEAREST)
 im.paste(src,(648*S,350*S))
 # Product labels remain readable; screenshots are visual evidence, not body copy.
 out=ROOT/'assets/atelier'/f'header-{mode}.png';out.parent.mkdir(parents=True,exist_ok=True)
 im.save(out,optimize=True)
 print(out.relative_to(ROOT))
 # Mobile: same elements restacked, without shrinking desktop type.
 mobile=Image.new('RGB',(640*S,720*S),bg)
 mobile.paste(im.crop((24*S,24*S,624*S,300*S)),(20*S,0))
 mobile.paste(im.crop((632*S,32*S,1168*S,448*S)),(52*S,288*S))
 mobile.save(ROOT/'assets/atelier'/f'header-{mode}-mobile.png',optimize=True)
