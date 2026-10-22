/** Original public demonstration stage. Edit this file to rebuild level structure. */
window.EmberLevels = Object.freeze({
  stage1: {
    name: '暮色回廊', width: 5400, groundY: 590, spawnX: 125,
    platforms: [
      [410,490,235,22],[790,420,210,22],[1110,480,260,22],
      [1510,425,200,22],[1830,505,190,22],[2180,445,255,22],
      [2580,500,250,22],[3010,420,230,22],[3490,465,240,22],
      [3890,405,185,22],[4630,490,260,22]
    ],
    enemies: [
      [740,'scout'],[1210,'scout'],[1660,'scout'],[2060,'brute'],
      [2400,'scout'],[2830,'brute'],[3270,'scout'],[3690,'brute']
    ],
    hazards: [[1010,1160],[2470,2580],[3780,3880]],
    crystals: [[550,445],[885,375],[1210,435],[1610,375],[2290,395],[2700,450],[3160,370],[3630,415],[4760,438]],
    boss: {x:4760,health:420}, exitX:5250
  }
});
