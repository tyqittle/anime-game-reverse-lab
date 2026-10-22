(function(){
  'use strict';
  const $=id=>document.getElementById(id);
  const canvas=$('gameCanvas'),prompt=$('gamePrompt'),start=$('startButton'),bossHud=$('bossHud');
  const audio=new window.EmberAudio();
  const game=new window.EmberEngine(canvas,audio,{
    hud(v){$('hpBar').style.width=`${100*v.hp/v.maxHp}%`;$('hpText').textContent=`${v.hp} / ${v.maxHp}`;
      $('score').textContent=String(v.score).padStart(6,'0');$('combo').textContent=`${v.combo} HIT`;
      $('distance').textContent=`距终端 ${v.distance}m`;$('objective').textContent=v.objective;
      bossHud.hidden=v.boss===null;$('bossBar').style.width=`${Math.max(0,(v.boss||0)*100)}%`;
    },
    toast(message,duration){const box=$('toast');box.textContent=message;box.classList.add('visible');clearTimeout(box._timer);box._timer=setTimeout(()=>box.classList.remove('visible'),Math.max(400,duration*1000))},
    finish(victory,score){prompt.style.display='flex';prompt.querySelector('.eyebrow').textContent=victory?'CHAPTER COMPLETE / MISSION ACCOMPLISHED':'MISSION FAILED / SIGNAL LOST';
      prompt.querySelector('h1').innerHTML=victory?'任务完成 <em>CLEAR</em>':'任务失败 <em>RETRY</em>';
      prompt.querySelector('p').textContent=`${victory?'你已解除终端守卫。':'你的信号已中断。'} 最终得分 ${score}。可以立即重开。`;
      start.innerHTML='重新挑战 <span>→</span>';game.keys.clear()}
  });
  start.addEventListener('click',()=>{prompt.style.display='none';game.start();canvas.focus({preventScroll:true})});
  const keyMap={KeyA:'a',KeyD:'d',KeyW:'w',KeyJ:'j',KeyK:'k',KeyL:'l',KeyP:'p',KeyR:'r',Space:'Space',ArrowLeft:'ArrowLeft',ArrowRight:'ArrowRight',ArrowUp:'ArrowUp',ShiftLeft:'Shift',ShiftRight:'Shift'};
  document.addEventListener('keydown',e=>{const key=keyMap[e.code];if(!key||e.target instanceof HTMLInputElement)return;e.preventDefault();if(key==='p'&&!e.repeat){game.togglePause();return}if(key==='r'&&!e.repeat){prompt.style.display='none';game.restart();return}game.key(key,true)});
  document.addEventListener('keyup',e=>{const key=keyMap[e.code];if(key)game.key(key,false)});
  window.addEventListener('blur',()=>{game.keys.clear();if(game.active&&!game.paused&&!game.finished&&!game.dead)game.togglePause()});
  $('soundButton').addEventListener('click',()=>{const on=audio.toggle();$('soundButton').textContent=`音效：${on?'开启':'关闭'}`;$('soundButton').setAttribute('aria-pressed',String(on));if(on)audio.play('coin')});
  $('skinFile').addEventListener('change',e=>{
    const file=e.target.files?.[0];if(!file)return;
    if(!['image/png','image/webp'].includes(file.type)||file.size>8*1024*1024){alert('请选择 8 MB 以内的 PNG 或 WebP 文件');return}
    const url=URL.createObjectURL(file),image=new Image();image.onload=()=>{
      if(game.spriteObjectURL)URL.revokeObjectURL(game.spriteObjectURL);
      game.spriteObjectURL=url;game.sprite=image;game.show('已加载本地角色贴图',2);
    };image.onerror=()=>{URL.revokeObjectURL(url);alert('图片无法解码')};image.src=url;
  });
  for(const b of document.querySelectorAll('[data-control]')){
    const key=b.dataset.control;
    const up=e=>{e.preventDefault();game.key(key,false)};
    b.addEventListener('pointerdown',e=>{e.preventDefault();b.setPointerCapture(e.pointerId);game.key(key,true)});
    b.addEventListener('pointerup',up);b.addEventListener('pointercancel',up);b.addEventListener('lostpointercapture',up);
  }
  window.__emberDebug={game,audio};
})();
