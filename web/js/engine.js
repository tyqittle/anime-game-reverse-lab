/* Project Ember - original 2D action simulation, no external game code or assets.
 * Engine/update/render are kept separate so the level and renderer can be swapped.
 */
(function(){
  'use strict';
  const W=1280,H=720,G=590,GRAVITY=1900,MAX_FALL=1050;
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const overlap=(a,b)=>a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
  const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
  const rnd=(a,b)=>a+Math.random()*(b-a);
  const rect=(ctx,x,y,w,h,color)=>{ctx.fillStyle=color;ctx.fillRect(x,y,w,h)};
  const path=(ctx,pts,color)=>{ctx.beginPath();ctx.moveTo(pts[0],pts[1]);for(let i=2;i<pts.length;i+=2)ctx.lineTo(pts[i],pts[i+1]);ctx.closePath();ctx.fillStyle=color;ctx.fill()};
  function capsule(ctx,x,y,w,h,r,color){ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill()}
  const level=window.EmberLevels.stage1;

  class Engine {
    constructor(canvas,audio,callbacks={}){
      this.canvas=canvas;this.ctx=canvas.getContext('2d',{alpha:false});this.audio=audio;this.callbacks=callbacks;
      this.keys=new Set();this.edge=new Set();this.active=false;this.paused=false;this.finished=false;this.dead=false;
      this.last=0;this.acc=0;this.time=0;this.frame=0;this.best=0;this.camera=0;this.shake=0;
      this.sprite=null;this.spriteObjectURL=null;this.reset();
      this._frame=this._frame.bind(this);requestAnimationFrame(this._frame);
    }
    reset(){
      this.player={x:level.spawnX,y:G-70,w:34,h:70,vx:0,vy:0,dir:1,hp:100,maxHp:100,inv:0,grounded:false,jumps:0,attack:0,attackHit:false,comboTimer:0,comboStep:0,dash:0,dashCD:0,shootCD:0,score:0,hitCombo:0,hitTimer:0};
      this.enemies=level.enemies.map(([x,type],i)=>({id:i,x,y:G-(type==='brute'?64:48),w:type==='brute'?54:39,h:type==='brute'?64:48,type,hp:type==='brute'?110:65,maxHp:type==='brute'?110:65,dir:-1,attackCD:rnd(.4,1.7),flash:0,vx:0}));
      this.boss={x:level.boss.x,y:G-145,w:115,h:145,hp:level.boss.health,maxHp:level.boss.health,dir:-1,flash:0,attackCD:2.2,phase:0,active:false,vx:0};
      this.crystals=level.crystals.map(([x,y])=>({x,y,taken:false}));this.bullets=[];this.particles=[];this.hits=[];
      this.camera=0;this.time=0;this.shake=0;this.finished=false;this.dead=false;this.paused=false;this.acc=0;
      this.emit();
    }
    start(){this.reset();this.active=true;this.keys.clear();this.edge.clear();this.show('开始任务：抵达终端',2)}
    restart(){this.reset();this.active=true;this.show('任务重新开始',1)}
    togglePause(){if(!this.active||this.finished||this.dead)return;this.paused=!this.paused;this.show(this.paused?'已暂停 / P 继续':'继续任务',1.5)}
    key(k,on){if(on){if(!this.keys.has(k))this.edge.add(k);this.keys.add(k)}else this.keys.delete(k)}
    pressed(...names){return names.some(k=>this.edge.has(k))}
    held(...names){return names.some(k=>this.keys.has(k))}
    show(text,duration=1.2){this.notice=text;this.noticeTime=duration;this.callbacks.toast?.(text,duration)}
    emit(){const p=this.player;this.callbacks.hud?.({hp:p.hp,maxHp:p.maxHp,score:p.score,combo:p.hitCombo,distance:Math.max(0,Math.ceil((level.exitX-p.x)/10)),boss:this.boss.active&&this.boss.hp>0?this.boss.hp/this.boss.maxHp:null,objective:this.boss.hp<=0?'抵达右侧撤离点':'抵达终端并清除守卫'})}
    _frame(t){
      const dt=Math.min((t-(this.last||t))/1000,.06);this.last=t;
      if(this.active&&!this.paused&&!this.finished&&!this.dead){this.acc+=dt;let n=0;while(this.acc>=1/60&&n<4){this.update(1/60);this.acc-=1/60;n++}if(n===4)this.acc=0}
      this.render();requestAnimationFrame(this._frame);
    }
    update(dt){
      const p=this.player;this.time+=dt;this.frame++;this.shake=Math.max(0,this.shake-dt*23);
      if(p.inv>0)p.inv-=dt;if(p.attack>0)p.attack-=dt;if(p.comboTimer>0)p.comboTimer-=dt;else p.comboStep=0;
      if(p.dash>0)p.dash-=dt;if(p.dashCD>0)p.dashCD-=dt;if(p.shootCD>0)p.shootCD-=dt;
      if(p.hitTimer>0)p.hitTimer-=dt;else p.hitCombo=0;
      this.updatePlayer(dt);this.updateEnemies(dt);this.updateBoss(dt);this.updateProjectiles(dt);this.updateParticles(dt);
      for(const c of this.crystals){if(!c.taken&&Math.hypot(c.x-(p.x+p.w/2),c.y-(p.y+p.h/2))<48){c.taken=true;p.score+=100;p.hp=Math.min(100,p.hp+5);this.audio.play('coin');this.spark(c.x,c.y,'#f6d5a5',13)}}
      if(p.hp<=0){this.dead=true;this.callbacks.finish?.(false,p.score);this.audio.play('hurt')}
      if(this.boss.hp<=0&&p.x>=level.exitX){this.finished=true;p.score+=1500;this.audio.play('win');this.callbacks.finish?.(true,p.score)}
      this.camera+=(clamp(p.x-350,0,level.width-W)-this.camera)*clamp(dt*6,0,1);
      if(this.frame%6===0)this.emit();this.edge.clear();
    }
    updatePlayer(dt){
      const p=this.player;
      if(this.pressed('Space','ArrowUp','w','jump')&&p.jumps<2){p.vy=p.jumps===0?-770:-680;p.grounded=false;p.jumps++;this.audio.play('jump');this.spark(p.x+17,p.y+p.h,'#93bfff',9)}
      if(this.pressed('k','Shift','dash')&&p.dashCD<=0){p.dash=.17;p.dashCD=.75;p.inv=Math.max(p.inv,.24);this.audio.play('dash');this.spark(p.x,p.y+35,'#9cdce7',15)}
      if(this.pressed('j','attack')&&p.attack<=0){p.comboStep=(p.comboTimer>0?p.comboStep+1:1)%4||1;p.attack=.22;p.attackHit=false;p.comboTimer=.45;this.audio.play('slash')}
      if(this.pressed('l','shoot')&&p.shootCD<=0){p.shootCD=.45;this.bullets.push({x:p.x+17+p.dir*23,y:p.y+28,vx:p.dir*700,vy:0,w:29,h:10,kind:'blade',time:1.5,damage:30});this.audio.play('shoot')}
      const m=(this.held('d','ArrowRight','right')?1:0)-(this.held('a','ArrowLeft','left')?1:0);
      if(m)p.dir=m;
      p.vx=p.dash>0?p.dir*980:m*325;
      p.x=clamp(p.x+p.vx*dt,0,level.width-p.w);
      const oldBottom=p.y+p.h;p.vy=clamp(p.vy+GRAVITY*dt,-1000,MAX_FALL);p.y+=p.vy*dt;p.grounded=false;
      if(p.vy>=0){let floor=G;for(const plat of level.platforms){const [x,y,w]=plat;if(p.x+p.w>x+5&&p.x<x+w-5&&oldBottom<=y+14&&p.y+p.h>=y&&y<floor)floor=y}if(p.y+p.h>=floor){p.y=floor-p.h;p.vy=0;p.grounded=true;p.jumps=0}}
      p.y=Math.min(p.y,H+200);
      if(p.y>H+80)this.damagePlayer(100,0);
      if(p.attack>.075&&!p.attackHit){const reach=80+p.comboStep*7;const hb={x:p.dir===1?p.x+p.w:p.x-reach,y:p.y+5,w:reach,h:65};let touched=false;
        for(const e of this.enemies){if(e.hp>0&&overlap(hb,e)){this.hitEnemy(e,33+p.comboStep*9,p.dir);touched=true}}
        if(this.boss.hp>0&&this.boss.active&&overlap(hb,this.boss)){this.hitBoss(25+p.comboStep*5,p.dir);touched=true}
        if(touched)p.attackHit=true;
      }
      for(const [left,right] of level.hazards){if(p.grounded&&p.x+p.w>left&&p.x<right){this.damagePlayer(22,p.x<left+25?-1:1);break}}
    }
    damagePlayer(damage,direction){
      const p=this.player;if(p.inv>0||this.dead||this.finished)return;
      p.hp=Math.max(0,p.hp-damage);p.inv=.85;p.vy=Math.min(-260,p.vy);p.x=clamp(p.x+direction*20,0,level.width-p.w);p.hitCombo=0;this.shake=9;this.audio.play('hurt');this.spark(p.x+17,p.y+35,'#ed807b',18);this.emit();
    }
    hitEnemy(e,dmg,direction){
      e.hp-=dmg;e.flash=.14;e.x+=direction*19;this.onHit(e.x+e.w/2,e.y+e.h/2,dmg);
      if(e.hp<=0){this.player.score+=e.type==='brute'?250:150;this.spark(e.x+e.w/2,e.y+25,'#a5cfff',24)}
    }
    hitBoss(dmg,direction){const b=this.boss;b.hp=Math.max(0,b.hp-dmg);b.flash=.1;b.x+=direction*7;this.onHit(b.x+b.w/2,b.y+60,dmg);if(b.hp===0){this.player.score+=2000;this.show('终端守卫已解除 / 前往撤离点',3);this.spark(b.x+50,b.y+65,'#f1b184',75);this.shake=19}}
    onHit(x,y,dmg){const p=this.player;p.hitCombo++;p.hitTimer=2.7;p.score+=Math.floor(dmg/3);this.shake=Math.max(this.shake,3);this.spark(x,y,'#f5c68b',11);this.audio.play('hit');this.hits.push({x,y,life:.5,text:String(dmg)})}
    updateEnemies(dt){const p=this.player;
      for(const e of this.enemies){if(e.hp<=0)continue;if(Math.abs(e.x-p.x)>880)continue;
        e.flash=Math.max(0,e.flash-dt);e.attackCD-=dt;
        const dx=p.x-e.x;e.dir=Math.sign(dx)||e.dir;
        if(Math.abs(dx)<390&&Math.abs(dx)>65)e.x+=Math.sign(dx)*(e.type==='brute'?75:105)*dt;
        if(Math.abs(dx)<e.w+45&&Math.abs(p.y-e.y)<85&&e.attackCD<=0){e.attackCD=e.type==='brute'?1.7:1.2;this.damagePlayer(e.type==='brute'?20:11,-e.dir)}
        if(e.type==='brute'&&Math.abs(dx)<380&&Math.abs(dx)>100&&e.attackCD<=0){e.attackCD=2;this.bullets.push({x:e.x,y:e.y+20,vx:e.dir*290,vy:0,w:17,h:17,kind:'enemy',time:2,damage:12})}
      }
    }
    updateBoss(dt){const b=this.boss,p=this.player;if(b.hp<=0)return;
      if(Math.abs(p.x-b.x)<660)b.active=true;
      if(!b.active)return;
      b.flash=Math.max(0,b.flash-dt);b.attackCD-=dt;b.dir=Math.sign(p.x-b.x)||-1;
      if(Math.abs(p.x-b.x)>155)b.x+=b.dir*(b.hp<b.maxHp*.5?108:74)*dt;
      if(b.attackCD<=0){b.attackCD=b.hp<b.maxHp*.5?1.05:1.85;b.phase++;const n=b.hp<b.maxHp*.5?5:3;
        for(let i=0;i<n;i++){const angle=Math.atan2((p.y+35)-(b.y+62),p.x-b.x)+(i-(n-1)/2)*.16;this.bullets.push({x:b.x+50,y:b.y+58,vx:Math.cos(angle)*360,vy:Math.sin(angle)*360,w:17,h:17,kind:'boss',time:3,damage:16})}
        this.spark(b.x+55,b.y+64,'#e990a5',18);
      }
      if(Math.abs(p.x-(b.x+b.w/2))<70&&Math.abs(p.y-b.y)<120)this.damagePlayer(23,b.dir);
    }
    updateProjectiles(dt){
      for(const z of this.bullets){z.x+=z.vx*dt;z.y+=z.vy*dt;z.time-=dt;if(z.time<=0)continue;
        if(z.kind==='blade'){
          for(const e of this.enemies){if(e.hp>0&&overlap(z,e)){this.hitEnemy(e,z.damage,Math.sign(z.vx));z.time=0;break}}
          if(z.time>0&&this.boss.hp>0&&this.boss.active&&overlap(z,this.boss)){this.hitBoss(z.damage,Math.sign(z.vx));z.time=0}
        }else if(overlap(z,this.player)){this.damagePlayer(z.damage,Math.sign(z.vx));z.time=0}
      }
      this.bullets=this.bullets.filter(z=>z.time>0&&z.x>-100&&z.x<level.width+100);
    }
    updateParticles(dt){for(const z of this.particles){z.x+=z.vx*dt;z.y+=z.vy*dt;z.vy+=330*dt;z.life-=dt}this.particles=this.particles.filter(z=>z.life>0);for(const z of this.hits)z.life-=dt;this.hits=this.hits.filter(z=>z.life>0)}
    spark(x,y,color,n){for(let i=0;i<n;i++){const t=rnd(0,Math.PI*2),v=rnd(80,330),life=rnd(.2,.7);this.particles.push({x,y,vx:Math.cos(t)*v,vy:Math.sin(t)*v,color,life,max:life,size:rnd(1.2,3.9)})}if(this.particles.length>380)this.particles.splice(0,this.particles.length-380)}

    render(){const c=this.ctx;c.clearRect(0,0,W,H);this.paintSky(c);c.save();c.translate(Math.round(-this.camera+rnd(-this.shake,this.shake)),Math.round(rnd(-this.shake,this.shake)));this.paintStage(c);
      for(const crystal of this.crystals)if(!crystal.taken)this.paintCrystal(c,crystal);
      for(const e of this.enemies)if(e.hp>0&&Math.abs(e.x-this.camera)<W+100)this.paintEnemy(c,e);
      if(this.boss.hp>0&&Math.abs(this.boss.x-this.camera)<W+200)this.paintBoss(c,this.boss);
      this.paintPlayer(c,this.player);
      this.paintBullets(c);
      for(const z of this.particles){c.globalAlpha=z.life/z.max;rect(c,z.x,z.y,z.size,z.size,z.color)}c.globalAlpha=1;
      c.font='bold 20px system-ui';c.textAlign='center';for(const z of this.hits){c.globalAlpha=clamp(z.life*2,0,1);c.fillStyle='#fff2ca';c.fillText(z.text,z.x,z.y-(.5-z.life)*45)}c.globalAlpha=1;c.restore();
      if(this.paused){rect(c,0,0,W,H,'#070b15a9');c.fillStyle='#f0d7b0';c.font='bold 44px system-ui';c.textAlign='center';c.fillText('PAUSED',W/2,H/2);c.font='18px system-ui';c.fillText('按 P 继续',W/2,H/2+38)}
    }
    paintSky(c){
      const grad=c.createLinearGradient(0,0,0,H);grad.addColorStop(0,'#152544');grad.addColorStop(.5,'#374568');grad.addColorStop(.82,'#d38c81');grad.addColorStop(1,'#40364b');rect(c,0,0,W,H,grad);
      c.save();c.globalAlpha=.8;const glow=c.createRadialGradient(994,255,15,994,255,260);glow.addColorStop(0,'#ffcfaa90');glow.addColorStop(1,'#fbc6a800');c.fillStyle=glow;c.fillRect(680,0,600,540);c.fillStyle='#f9d9b8';c.beginPath();c.arc(995,225,68,0,Math.PI*2);c.fill();c.restore();
      for(let l=0;l<3;l++){let offset=this.camera*(.05+l*.11),base=400+l*56,alpha=.13+l*.15;c.fillStyle=l===0?'#23335d':l===1?'#27324c':'#263044';c.globalAlpha=alpha+.24;
        c.beginPath();c.moveTo(0,H);for(let x=-180;x<W+300;x+=75){const wx=x+offset;const y=base+Math.sin(wx*.006+l)*44+Math.sin(wx*.014+l*2)*24;c.lineTo(x,y)}c.lineTo(W,H);c.fill();c.globalAlpha=1}
      const shift=this.camera*.31;c.fillStyle='#18263c';for(let i=-1;i<30;i++){const x=i*105-shift%105,w=55+(i*73)%70,h=105+(i*41)%105;c.fillRect(x,468-h,w,h+245);for(let j=0;j<5;j++){c.fillStyle=i%4?'#f4a78c33':'#f7d4a133';c.fillRect(x+12+j*9,482-h+19,3,6)}c.fillStyle='#18263c'}
      for(let i=0;i<45;i++){const x=((i*273-this.camera*.12)%1420+1420)%1420,y=90+i*83%420;c.fillStyle=i%3?'#f6dac248':'#b0d5ff33';c.fillRect(x,y,2,2)}
    }
    paintStage(c){
      rect(c,0,G,level.width,H-G,'#1b2632');rect(c,0,G-12,level.width,12,'#485362');rect(c,0,G-14,level.width,2,'#dca382');
      for(let x=0;x<level.width;x+=96){if(x<this.camera-120||x>this.camera+W+120)continue;rect(c,x,G+11,2,H-G-11,'#6272821b');rect(c,x+40,G+43,54,2,'#d9c6a510')}
      for(const [x,y,w,h] of level.platforms){if(x+w<this.camera-30||x>this.camera+W+30)continue;rect(c,x,y,w,h,'#3c465c');rect(c,x,y,w,4,'#e3ac8e');rect(c,x+7,y+14,w-14,3,'#283341');rect(c,x+20,y+h,10,32,'#27374c');rect(c,x+w-30,y+h,10,32,'#27374c')}
      for(const [x,r] of level.hazards){rect(c,x,G-4,r-x,9,'#d96e67');for(let a=x;a<r;a+=20)path(c,[a,G+5,a+10,G-12,a+20,G+5],'#faab8c')}
      for(let x=230;x<level.width;x+=560){if(x<this.camera-100||x>this.camera+W+100)continue;rect(c,x,G-145,14,145,'#34445a');rect(c,x-17,G-156,48,14,'#465773');rect(c,x+4,G-145,5,130,'#d9a97e40');rect(c,x-50,G-160,114,4,'#7a849a')}
      rect(c,level.exitX,G-165,10,165,'#c88d87');rect(c,level.exitX+88,G-165,10,165,'#c88d87');rect(c,level.exitX,G-165,98,10,'#e3b79b');
      const arch=c.createLinearGradient(level.exitX,0,level.exitX+98,0);arch.addColorStop(0,'#64c9e333');arch.addColorStop(.5,'#71efff7a');arch.addColorStop(1,'#64c9e333');rect(c,level.exitX+12,G-152,76,148,arch);
    }
    paintCrystal(c,z){const glow=.5+Math.sin(this.time*4+z.x)*.24;c.save();c.translate(z.x,z.y+Math.sin(this.time*3+z.x)*6);c.rotate(Math.PI/4);c.shadowColor='#fff0be';c.shadowBlur=25*glow;rect(c,-11,-11,22,22,'#edc891');rect(c,-5,-5,10,10,'#fff7d6');c.restore()}
    paintEnemy(c,e){c.save();c.translate(e.x,e.y);if(e.flash>0)c.globalAlpha=.5;
      if(e.type==='brute'){capsule(c,4,8,46,52,8,'#3f3c54');rect(c,0,18,54,19,'#7e5365');capsule(c,7,0,40,29,11,'#505b76');rect(c,10,9,34,6,'#f4a09c');rect(c,10,53,14,11,'#303447');rect(c,34,53,14,11,'#303447');rect(c,e.dir===1?50:-12,20,15,25,'#9e7181')}
      else{capsule(c,5,11,29,32,9,'#4b526c');capsule(c,0,2,39,27,12,'#333e53');rect(c,8,14,23,5,'#e88c9b');rect(c,5,40,10,8,'#252c3d');rect(c,25,40,10,8,'#252c3d');rect(c,e.dir===1?34:-7,28,11,6,'#a8707d')}
      c.restore();if(e.hp<e.maxHp){rect(c,e.x,e.y-17,e.w,4,'#384659');rect(c,e.x,e.y-17,e.w*clamp(e.hp/e.maxHp,0,1),4,'#f49b92')}
    }
    paintBoss(c,b){c.save();c.translate(b.x,b.y);if(b.flash>0)c.globalAlpha=.65;
      c.shadowColor='#f39b9b';c.shadowBlur=25;path(c,[56,-35,80,10,106,40,85,86,55,108,20,88,0,45,29,10],'#6e526b');c.shadowBlur=0;
      path(c,[15,42,58,23,102,48,109,119,80,140,42,139,9,117],'#293650');
      capsule(c,35,0,49,57,18,'#56627c');path(c,[25,22,95,22,84,58,36,58],'#29334b');rect(c,42,32,39,6,'#f5a0a7');
      rect(c,30,60,58,56,'#45536d');path(c,[-25,37,-3,19,23,61,10,77],'#bb7b80');path(c,[104,42,130,15,143,25,110,85],'#bb7b80');
      path(c,[42,112,61,112,54,145,31,145],'#242d3b');path(c,[67,112,86,112,99,145,74,145],'#242d3b');
      c.restore()}
    paintPlayer(c,p){c.save();c.translate(p.x+p.w/2,p.y+p.h);c.scale(p.dir,1);if(p.inv>0&&Math.floor(this.time*15)%2===0)c.globalAlpha=.5;
      if(p.dash>0){c.globalAlpha=.25;rect(c,-p.dir*33-40,-70,43,65,'#b4efff')}
      if(this.sprite){
        const img=this.sprite;const scale=Math.min(100/img.width,92/img.height);const w=img.width*scale,h=img.height*scale;c.drawImage(img,-w/2,-h+5,w,h);
      }else{
        // Original vector ninja: animated scarf, hair, cloak and blade.
        const stride=p.grounded?Math.sin(this.time*(Math.abs(p.vx)>4?17:2))*9:4;
        path(c,[-5,-50,-38-Math.sin(this.time*8)*12,-63,-29,-54,-5,-38],'#d08087');
        path(c,[-6,-48,-27,-25,-11,-6,19,-14,24,-48],'#293b59');
        path(c,[-7,-23,2,-20,-1+stride,0,-13,0],'#151c2e');path(c,[8,-22,20,-22,16-stride,0,2,0],'#151c2e');
        capsule(c,-11,-60,29,39,8,'#f0e7da');path(c,[-11,-56,17,-51,19,-23,-9,-26],'#49607a');
        path(c,[-13,-68,-5,-85,20,-76,22,-62,8,-54,-8,-56],'#1d2437');
        path(c,[-13,-70,-29,-81,-20,-64,-11,-62],'#222f47');
        path(c,[5,-65,17,-61,14,-57,6,-59],'#f3d3b0');rect(c,10,-63,4,2,'#b35464');
        path(c,[-13,-58,-27,-45,-18,-30,-9,-41],'#56667e');path(c,[12,-51,27,-36,17,-31,6,-43],'#c7b3af');
        // scabbard
        path(c,[-17,-17,5,-41,10,-38,-9,-12],'#c8a178');
      }
      if(p.attack>0){const a=(1-p.attack/.22)*Math.PI*.95-.45;c.save();c.rotate(a);c.shadowColor='#fff6df';c.shadowBlur=22;path(c,[17,-52,100,-85,118,-83,26,-43],'#fff0d5');path(c,[17,-53,103,-80,29,-41],'#9bd9f0');c.restore();c.strokeStyle='#f6d8b9ba';c.lineWidth=7;c.beginPath();c.arc(0,-44,86,-.85,1.15);c.stroke()}
      c.restore()}
    paintBullets(c){for(const b of this.bullets){if(b.kind==='blade'){c.save();c.translate(b.x,b.y);c.rotate(this.time*18);path(c,[-25,-2,0,-7,25,2,0,7],'#d6eeff');c.restore()}else{c.fillStyle=b.kind==='boss'?'#e9a2bd':'#f0b199';c.shadowColor=c.fillStyle;c.shadowBlur=15;c.beginPath();c.arc(b.x+8,b.y+8,b.w/2,0,Math.PI*2);c.fill();c.shadowBlur=0}}}
  }
  window.EmberEngine=Engine;
})();
