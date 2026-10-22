/** Tiny original oscillator-based SFX; no external audio, no autoplay. */
(function(){
 class AudioFX {
   constructor(){this.enabled=false;this.ctx=null}
   toggle(){this.enabled=!this.enabled;return this.enabled}
   play(name){
     if(!this.enabled)return;
     try {
       const A=window.AudioContext||window.webkitAudioContext;
       if(!A)return;
       if(!this.ctx)this.ctx=new A();
       if(this.ctx.state==='suspended')this.ctx.resume();
       const map={jump:[450,720,.12,'sine'],hit:[145,54,.15,'sawtooth'],slash:[920,210,.11,'triangle'],dash:[90,260,.19,'triangle'],shoot:[620,240,.12,'square'],hurt:[180,60,.22,'sawtooth'],coin:[600,960,.22,'sine'],win:[620,1140,.5,'sine']};
       const [from,to,length,shape]=map[name]||map.jump;
       const o=this.ctx.createOscillator(),g=this.ctx.createGain(),t=this.ctx.currentTime;
       o.type=shape;o.frequency.setValueAtTime(from,t);o.frequency.exponentialRampToValueAtTime(Math.max(to,1),t+length);
       g.gain.setValueAtTime(.065,t);g.gain.exponentialRampToValueAtTime(.001,t+length);
       o.connect(g);g.connect(this.ctx.destination);o.start(t);o.stop(t+length+.02);
     }catch(_err){} // Sound must never interrupt gameplay.
   }
 }
 window.EmberAudio=AudioFX;
})();
