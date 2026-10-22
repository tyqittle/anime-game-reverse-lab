// Zero-dependency headless mechanics tests (Node 20+).
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.join(__dirname,'../web/js');
const sandbox={window:{},requestAnimationFrame(){},console,Math,Image:function(){}};
vm.createContext(sandbox);
for(const src of ['levels.js','audio.js','engine.js'])vm.runInContext(readFileSync(path.join(root,src),'utf8'),sandbox,{filename:src});
function game(){
  const callbacks={hud(){},toast(){},finish(){}};
  const fakeCanvas={getContext(){return {}}};
  const e=new sandbox.window.EmberEngine(fakeCanvas,{play(){}},callbacks);
  e.start();return e;
}
test('stage has navigable platforms, enemies, hazards and boss',()=>{
 const s=sandbox.window.EmberLevels.stage1;
 assert.ok(s.width>s.exitX);assert.ok(s.platforms.length>5);
 assert.ok(s.enemies.length>=8);assert.ok(s.hazards.length>=2);
 assert.ok(s.boss.x<s.exitX);
});
test('A/D movement and double jump are simulated',()=>{
 const g=game(),x=g.player.x;
 g.key('d',true);for(let i=0;i<40;i++)g.update(1/60);
 assert.ok(g.player.x>x+150);g.key('d',false);
 g.key('Space',true);g.update(1/60);g.key('Space',false);g.update(1/60);
 assert.equal(g.player.jumps,1);const v=g.player.vy;
 g.key('Space',true);g.update(1/60);assert.equal(g.player.jumps,2);assert.ok(g.player.vy<-600&&g.player.vy>v);
});
test('attack, projectile, dash, restart and victory conditions',()=>{
 const g=game();g.key('j',true);g.update(1/60);assert.ok(g.player.attack>0);g.key('j',false);
 g.key('l',true);g.update(1/60);assert.ok(g.bullets.some(b=>b.kind==='blade'));g.key('l',false);
 g.key('k',true);g.update(1/60);assert.ok(g.player.dashCD>0);g.restart();assert.equal(g.bullets.length,0);
 g.boss.hp=0;g.player.x=5300;g.update(1/60);assert.equal(g.finished,true);
});
test('damage prevents immediate repeated injury during invulnerability',()=>{
 const g=game();g.damagePlayer(15,1);assert.equal(g.player.hp,85);
 g.damagePlayer(15,1);assert.equal(g.player.hp,85);
});
