// Controllo: i valori letti dal template NUOVO sono identici a quelli letti dal template di OGGI.
// uso: node controllo_valori.js dati_vecchi.json dati_nuovi.json template_vecchio.html template_nuovo.html
const fs=require("fs"), assert=require("assert");
const [,, fv, fn, tv, tn]=process.argv;
const Dv=JSON.parse(fs.readFileSync(fv,"utf8")), Dn=JSON.parse(fs.readFileSync(fn,"utf8"));
const tvec=fs.readFileSync(tv,"utf8"), tnuo=fs.readFileSync(tn,"utf8");
const px = lon => (lon+180)/360;
const py = lat => { const s=Math.sin(lat*Math.PI/180); return 0.5-Math.log((1+s)/(1-s))/(4*Math.PI); };
// --- lettore vecchio: espandiAcc dal template di oggi
const mAcc=tvec.match(/const GRUPPI_ACC[\s\S]*?\n\}\n/)[0];
// --- lettore nuovo: blocco DECODIFICA del template nuovo
const blocco=tnuo.slice(tnuo.indexOf("/* DECODIFICA:INIZIO"), tnuo.indexOf("/* DECODIFICA:FINE */"));
const D={fermate:Dn.fermate};
const vec=new Function("px","py",mAcc+"; return {espandiAcc, GRUPPI_ACC};")(px,py);
const nuo=new Function("px","py","D",blocco+"; return {espandiAcc,espandiVcomp,espandiFb,espandiForma,espandiRiquadro,espandiFermate,GRUPPI_ACC};")(px,py,D);
const C=Dn.sezioni, V=Dv.sezioni;
assert.strictEqual(C.n, V.length);
// campione di 200 sezioni (seme fisso) + tutte
let seed=12345; const rnd=()=>(seed=(seed*1103515245+12345)%2147483648)/2147483648;
const campione=new Set(); while(campione.size<200) campione.add(Math.floor(rnd()*V.length));
let confronti=0, diff=0, diffCamp=0;
function eq(a,b,dove,i){ confronti++; try{ assert.deepStrictEqual(a,b); }catch(e){ diff++; if(campione.has(i)) diffCamp++; if(diff<=5) console.log("DIVERSO",dove,i,JSON.stringify(a).slice(0,120),JSON.stringify(b).slice(0,120)); } }
const rows=["p","c","f","occ","p1564","sen","p014","em","ist9","it","pf1","pf3","v"];
let valoriAcc=0, valoriCamp=0;
for(let i=0;i<V.length;i++){
  const z=V[i];
  const aV=vec.espandiAcc(z.acc), aN=nuo.espandiAcc(C.acc[i]);
  eq(aN,aV,"acc",i);
  // valore per valore: 5 gruppi x (a piedi + 24 ore), come li legge il template (accGrezzo / accValore)
  for(const g of vec.GRUPPI_ACC){
    const lett=(a,h)=>h==null?(a.piedi||{})[g]:((a.tp||{})[String(h).padStart(2,"0")]||{})[g];
    for(const h of [null,...Array(24).keys()]){ valoriAcc++; if(campione.has(i)) valoriCamp++; eq(lett(aN,h),lett(aV,h),"acc["+g+","+h+"]",i); }
  }
  // vcomp: i 4 campi che il template legge
  const vcV=z.vcomp||{}, vcN=nuo.espandiVcomp(C.vc[i]);
  for(const k of ["occ","ist","aff","anz"]) eq(vcN[k],vcV[k],"vcomp."+k,i);
  eq(nuo.espandiFb(C.fb[i]),z.fb||{},"fb",i);
  eq(C.r1[i]||null,z.r1||null,"r1",i);
  eq(C.a[i],z.a,"km2",i);
  for(const k of rows) eq(C[k][i],z[k],k,i);
  // centro e riquadro: identici a quelli calcolati dalle forme originali
  let x0=1,y0=1,x1=0,y1=0;
  for(const a of z.g) for(const p of a){ const X=px(p[1]),Y=py(p[0]); x0=Math.min(x0,X);x1=Math.max(x1,X);y0=Math.min(y0,Y);y1=Math.max(y1,Y); }
  eq(nuo.espandiRiquadro(C.bb[i]),[x0,y0,x1,y1],"riquadro",i);
  // forme: stesso numero di anelli, anelli chiusi con almeno 4 punti
  const poly=nuo.espandiForma(C.g[i]);
  eq(poly.length,z.g.length,"n.anelli",i);
  for(const a of poly){ eq(a.length/2>=4 && a[0]===a[a.length-2] && a[1]===a[a.length-1],true,"anello chiuso>=4",i); }
}
// fermate: passaggi per ora
nuo.espandiFermate();
for(let i=0;i<Dv.fermate.length;i++){ eq(Dn.fermate[i].d,Dv.fermate[i].d,"fermata.d",i); eq([Dn.fermate[i].id,Dn.fermate[i].n,Dn.fermate[i].la,Dn.fermate[i].lo,Dn.fermate[i].r],[Dv.fermate[i].id,Dv.fermate[i].n,Dv.fermate[i].la,Dv.fermate[i].lo,Dv.fermate[i].r],"fermata.campi",i); }
console.log(`sezioni: ${V.length} (tutte); campione di 200: ${[...campione].length}; valori di accessibilita' confrontati: ${valoriAcc} (nel campione: ${valoriCamp}, = 200 x 5 gruppi x 25)`);
console.log(`confronti: ${confronti}; differenze: ${diff} (nel campione: ${diffCamp})`);
process.exit(diff?1:0);
