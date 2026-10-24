const { chromium } = require('playwright');
(async()=>{
  const b = await chromium.launch(); 
  const list=[['a_podcast',1280,720],['b_interview',1080,1920],['c_announce',1280,720],['c_announce2',1280,720],['d_creators',1280,720],['e_ycs',1280,720],['f_nyumon',1280,720]];
  for (const [n,w,h] of list){
    const p = await b.newPage({viewport:{width:w,height:h}});
    await p.goto('file://'+process.cwd()+'/'+n+'.html'); await p.waitForTimeout(1500);
    await p.evaluate(()=>document.fonts.ready);
    await p.screenshot({path:n+'.png'}); await p.close();
  }
  await b.close();
})();
