'use strict';
class APIError extends Error {
 constructor(message, errors=[]) { super(message); this.errors=errors; }
}
async function requestAPI(path, {query, body, signal}={}) {
 const url=new URL(path,window.location.origin);
 if(query) for(const [key,value] of Object.entries(query)) if(value!==undefined&&value!==null) url.searchParams.set(key,value);
 const timeout=new AbortController();
 const timer=setTimeout(()=>timeout.abort(),30000);
 const abort=()=>timeout.abort();
 if(signal) { if(signal.aborted) abort(); else signal.addEventListener('abort',abort,{once:true}); }
 try {
  const response=await fetch(url,{method:body===undefined?'GET':'POST',headers:body===undefined?{Accept:'application/json'}:{Accept:'application/json','Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body),signal:timeout.signal,cache:'no-store'});
  let data;
  try { data=await response.json(); } catch { throw new APIError('The server returned an unreadable response. Restart the prototype server and try again.'); }
  if(!response.ok) throw new APIError(data.error||data.errors?.join(' ')||`Request failed (${response.status}).`,data.errors||[]);
  return data;
 } catch(error) {
  if(error instanceof APIError) throw error;
  if(error.name==='AbortError') throw new APIError('The request was interrupted or timed out. Please try again.');
  throw new APIError('Cannot reach the backend. Start the prototype server and try again.');
 } finally {
  clearTimeout(timer);if(signal)signal.removeEventListener('abort',abort);
 }
}

const $=id=>document.getElementById(id);
const esc=s=>String(s??'—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(n);
const option=(value,label)=>`<option value="${esc(value)}">${esc(label)}</option>`;
const placeholder=()=>option('','Please Select');
let page=1;
const PAGE_SIZE=1;

const link=(url,label)=>/^https?:\/\//i.test(url||'')?`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`:'No link recorded';
const fields=['cancer','regimen','subtype','age','size','address','state','county','income','otherIncome','expenses','children','ageGroup','missedHours','hourly','insurance','deductible','coinsurance','cap'];
const numeric=['age','size','income','otherIncome','expenses','children','missedHours','hourly','deductible','coinsurance','cap'];
const CASES=[
 {cancer:'BREAST',age:42,size:3,location:'durham_demo',income:54000,otherIncome:6000,expenses:3000,children:1,ageGroup:'PRESCHOOL',missedHours:4,hourly:22,insurance:'Private',deductible:1500,coinsurance:20,cap:7000},
 {cancer:'LUNG',age:72,size:2,location:'greenville_demo',income:0,otherIncome:29000,expenses:2000,children:0,ageGroup:'SCHOOL_AGE',missedHours:0,hourly:0,insurance:'Medicare',deductible:500,coinsurance:20,cap:9000},
 {cancer:'LYMPHOMA',age:20,size:1,location:'charlotte_demo',income:0,otherIncome:0,expenses:900,children:0,ageGroup:'PRESCHOOL',missedHours:0,hourly:0,insurance:'Uninsured',deductible:0,coinsurance:100,cap:0},
 {cancer:'PROSTATE',age:60,size:2,location:'raleigh_demo',income:220000,otherIncome:0,expenses:5000,children:0,ageGroup:'PRESCHOOL',missedHours:3,hourly:65,insurance:'Private',deductible:2000,coinsurance:20,cap:8000}
];
const DATA={cancer_type:[],regimen:[],hospital:[],county:[]};
const details=new Map();
const norm=s=>String(s??'').trim().toLowerCase();
let HOSPITAL_IDS=[];
let current=null, resolvedAddress=null, profileVersion=0, regimenVersion=0, detailVersion=0;
function setBusy(busy,message='Calculating treatment costs…'){
 $('load').disabled=busy;$('compareButton').disabled=busy;
 $('requestStatus').hidden=!busy;$('requestStatus').textContent=message;
 $('profile').setAttribute('aria-busy',String(busy));
}
function showRequestError(error){showFormErrors(error.errors?.length?error.errors:[error.message||String(error)]);}
async function fetchDetail(id){
 if(!details.has(id))details.set(id,await requestAPI('/api/regimen-detail',{query:{regimen:id}}));
 return details.get(id);
}
async function updateRegimen(){
 const version=++regimenVersion,cancer=$('cancer').value;
 ++detailVersion;
 $('regimen').innerHTML=placeholder();$('subtype').innerHTML=placeholder();$('regimenInfo').innerHTML='';
 $('regimen').disabled=true;
 if(!cancer)return;
 try {
  const [regimens,subtypes]=await Promise.all([
   requestAPI('/api/regimens',{query:{cancer}}),requestAPI('/api/assistance-subtypes',{query:{cancer}})
  ]);
  if(version!==regimenVersion)return;
  for(const r of regimens){const index=DATA.regimen.findIndex(x=>x.regimen_id===r.regimen_id);const row={...r,name:r.regimen};if(index<0)DATA.regimen.push(row);else DATA.regimen[index]=row;}
  $('regimen').innerHTML=placeholder()+regimens.map(r=>option(r.regimen_id,r.regimen)).join('');
  $('subtype').innerHTML=placeholder()+subtypes.map(value=>option(value,value)).join('');
 } finally { if(version===regimenVersion)$('regimen').disabled=false; }
}
async function regimenInfo(){
 const version=++detailVersion,id=$('regimen').value;
 $('regimenInfo').innerHTML='';
 if(!id)return;
 const detail=await fetchDetail(id);
 if(version!==detailVersion||id!==$('regimen').value)return;
 $('regimenInfo').innerHTML=`<p>
<strong>${detail.total_visits} visits · ${detail.total_weeks} weeks</strong>
<br>${link(detail.source_url,'Seeded regimen reference')}</p>
<details class="debug">
<summary>Phases before estimating</summary>${phaseTable(id)}</details>`;
}
function phaseTable(id){return `<div class="tablewrap">
<table>
<thead>
<tr>
<th>Phase / treatment</th>
<th>Start week</th>
<th>Cycles × visits</th>
<th>Cycle days</th>
</tr>
</thead>
<tbody>${(details.get(id)?.phases||[]).map(r=>`<tr>
<td>${r.phase}. ${esc(r.treatment)}</td>
<td>${r.start_week}</td>
<td>${r.cycles} × ${r.visits_per_cycle}</td>
<td>${r.cycle_days}</td>
</tr>`).join('')}</tbody>
</table>
</div>`;}
async function setLocation(){
 const selected=$('location').value;
 if(!selected){resolvedAddress=null;$('address').value='';$('state').value='';$('county').value='';HOSPITAL_IDS.forEach(h=>$('distance_'+h).value='');return;}
 const row=await requestAPI('/api/addresses/'+encodeURIComponent(selected));
 if($('location').value!==selected) return; // Ignore a stale asynchronous lookup.
 resolvedAddress=row;
 $('address').value=row.street_address+', '+row.city+', '+row.state;
 $('county').value=row.county;$('state').value=row.state;
 HOSPITAL_IDS.forEach(h=>$('distance_'+h).value=row.distances_miles[h]);
}
async function loadCase(){
 if($('scenario').value===''){showFormErrors(['Please select a test household first.']);return;}
 setBusy(true,'Loading the sample household…');
 $('stale').hidden=!current;
 const version=++profileVersion;
 try {
  const p=CASES[+$('scenario').value];
  for(const key of fields)if(key in p)$(key).value=p[key];
  $('subtype').value='';$('location').value=p.location;
  await updateRegimen();if(version!==profileVersion)return;
  $('regimen').value=DATA.regimen.find(r=>r.cancer_id===p.cancer).regimen_id;
  await Promise.all([regimenInfo(),setLocation()]);if(version!==profileVersion)return;
  updateConditionalFields();clearFilters();await run();
 } catch(error){if(version===profileVersion)showRequestError(error);}
 finally {setBusy(false);}
}
function showFormErrors(errors){$('errors').hidden=!errors.length;$('errors').className='error';$('errors').innerHTML='<strong>Check the profile:</strong><ul>'+errors.map(e=>`<li>${esc(e)}</li>`).join('')+'</ul>';}
function updateConditionalFields(){
 const uninsured=$('insurance').value==='Uninsured';
 const childcare=Number($('children').value)>0;
 for(const id of ['deductible','coinsurance','cap']){$(id).required=!uninsured;$(id).disabled=uninsured;}
 $('childcareAgeField').hidden=!childcare;
 $('ageGroup').required=childcare;$('ageGroup').disabled=!childcare;
 const lostPay=Number($('missedHours').value)>0;
 $('hourlyPayField').hidden=!lostPay;
 $('hourly').required=lostPay;$('hourly').disabled=!lostPay;
 for(const el of document.querySelectorAll('#profile input,#profile select')){
  const label=document.querySelector(`label[for="${el.id}"]`);if(label)label.classList.toggle('required-label',el.required&&!el.disabled);
 }
}
function readProfile(){const p=Object.fromEntries(fields.map(k=>[k,numeric.includes(k)?($(k).value.trim()===''?NaN:Number($(k).value)):$(k).value]));p.distances=HOSPITAL_IDS.map(h=>$('distance_'+h).value.trim()===''?NaN:Number($('distance_'+h).value));if(!(p.missedHours>0))p.hourly=0;p.addressId=resolvedAddress?.address_id;p.city=resolvedAddress?.city;p.distanceSource=resolvedAddress?.source;p.distanceOverrides=HOSPITAL_IDS.some((h,i)=>p.distances[i]!==resolvedAddress?.distances_miles[h]);return p;}
async function run(){
 const version=profileVersion;
 setBusy(true);showFormErrors([]);
 try {
  if(resolvedAddress?.address_id!==$('location').value) await setLocation();
  if(version!==profileVersion)return;
  const result=await requestAPI('/api/compare',{body:readProfile()});
  await fetchDetail(result.profile.regimen);
  if(version!==profileVersion)return;
  current=result;page=1;$('searchOutput').hidden=false;$('stale').hidden=true;
 const f=result.finances;
 $('financial').innerHTML=`<div class="metrics">
<div class="metric">Annual gross income<strong>${esc(money(f.annual))}</strong>
</div>
<div class="metric">2026 poverty guideline<strong>${money(f.guideline)}</strong>
</div>
<div class="metric">Income / FPL<strong>${esc(f.fpl.toFixed(1)+'%')}</strong>
</div>
<div class="metric">Monthly gross income<strong>${esc(money(f.monthly))}</strong>
</div>
<div class="metric">Usual monthly expenses<strong>${esc(money(result.profile.expenses))}</strong>
</div>
<div class="metric">Monthly income left for treatment<strong>${esc(money(f.available))}</strong>
</div>
</div>
<p class="small">Earnings + benefits / other income, before taxes. Disposable income = max(0, monthly gross income − usual expenses). ${f.annual===0?'Zero income: percentage burden is undefined; costs and funding gaps are still ranked.':''}</p>`;
 render();
 } catch(error){if(version===profileVersion){showRequestError(error);$('stale').hidden=!current;}}
 finally {setBusy(false);}
}
function aidCard(a){return `<div class="aid">
<strong>${esc(a.program_name)}</strong> <span class="badge warn">${esc(a.status)}</span>
<p>${esc(a.organization)} · ${esc(a.assistance_type)}<br>
<strong>Recorded benefit:</strong> ${esc(a.assistance_amount||'Not specified')}</p>
<p class="small">Income limit: ${a.income_limit_fpl==null?'not recorded':a.income_limit_fpl+'% FPL'} · age: ${a.min_age??'no min'}–${a.max_age??'no max'} · insurance: ${esc(a.accepted_insurance.join(', ')||'no restriction recorded')}</p>${a.reasons.length?'<p class="error">'+esc(a.reasons.join('; '))+'</p>':''}<p>${link(a.application_url,'Application / program page')} · ${link(a.source_url,'Seeded source')}</p>
<details class="debug">
<summary>All requirements, geography & source record</summary>${a.review.map(r=>`<p>${esc(r)}</p>`).join('')}<pre>${esc(JSON.stringify(a,null,2))}</pre>
</details>
</div>`;}
function render(){
 if(!current)return;
 const aidText=norm($('aidType').value);
 const hasAid=a=>!aidText||norm(a.assistance_type).includes(aidText);
 let rows=current.results.filter(r=>(!$('hospitalFilter').value||r.hospital_id===$('hospitalFilter').value)&&($('maxDistance').value===''||r.distance<=Number($('maxDistance').value))&&($('maxCost').value===''||r.total<=Number($('maxCost').value))&&($('eligibility').value!=='eligible'||r.eligible));
 if($('sort').value&&$('sort').value!=='recommended') rows.sort((a,b)=>$('sort').value==='medical'?a.costs.medical-b.costs.medical:a[$('sort').value]-b[$('sort').value]);
 const count=rows.length,pages=Math.max(1,Math.ceil(count/PAGE_SIZE));page=Math.min(Math.max(page,1),pages);
 const navigation=()=>`<nav class="pagination" aria-label="Results pages">
<button type="button" data-page="1" ${page===1?'disabled':''}>First</button>
<button type="button" data-page="${page-1}" ${page===1?'disabled':''}>Previous</button>
<span>Page ${page} of ${pages} · ${count} results</span>
<button type="button" data-page="${page+1}" ${page===pages?'disabled':''}>Next</button>
<button type="button" data-page="${pages}" ${page===pages?'disabled':''}>Last</button>
</nav>`;
 $('results').innerHTML=`<h2>${rows.length} of ${current.results.length} hospital programs</h2>${rows.length?'':'<section>No hospital programs meet these filters. Clear filters or revise the profile.</section>'}`+navigation()+rows.slice((page-1)*PAGE_SIZE,page*PAGE_SIZE).map((r,i)=>{
 const aid=r.assistance.filter(a=>!a.reasons.length&&hasAid(a)), excluded=r.assistance.filter(a=>a.reasons.length&&hasAid(a));
 const labels={medical:'Medical out of pocket',travel:'Round-trip transportation',lodging:'Overnight lodging',meals:'Meals during overnight stays',childcare:'Childcare',lostWages:'Lost wages'};
 const regimen=DATA.regimen.find(x=>x.regimen_id===current.profile.regimen);
 return `<article>
<span class="badge">Display #${(page-1)*PAGE_SIZE+i+1} · financial rank #${current.results.indexOf(r)+1}</span>
<span class="badge ${r.eligible?'':'warn'}">${esc(r.eligible?'Passes sample rules':'Does not pass sample rules')}</span>
<h2>${esc(r.name)}</h2>
<p>${esc(r.city)}, NC · ${esc(r.county)} County · ${esc(r.distance)} sample one-way miles</p>
<p>
<strong>${esc(regimen.name)}</strong>
<br>${r.summary.visits} visits over ${r.summary.weeks} weeks (~${r.months.toFixed(1)} months). <span class="prototype-note">${esc(r.eligibilityReason)}</span>
</p>
<div class="metrics">
<div class="metric">Total course burden<strong>${esc(money(r.total))}</strong>
<small>Course range: ${esc(money(r.totalMin))}–${esc(money(r.totalMax))}</small>
</div>
<div class="metric">Gap after available income<strong>${esc(money(r.gap))}</strong>
</div>
<div class="metric">Cost / course gross income<strong>${esc(r.burden===null?'N/A':r.burden.toFixed(1)+'%')}</strong>
</div>
</div>
<div class="tablewrap">
<table>
<thead>
<tr>
<th>Course cost item</th>
<th class="right">Estimate</th>
</tr>
</thead>
<tbody>${Object.entries(r.costs).map(([k,v])=>`<tr>
<td>${labels[k]}</td>
<td class="right">${money(v)}</td>
</tr>`).join('')}<tr>
<th>Total (before assistance)</th>
<th class="right">${esc(money(r.total))}</th>
</tr>
</tbody>
</table>
</div>
<p>Medical OOP range: ${esc(money(r.medicalMin))}–${esc(money(r.medicalMax))}. <span class="prototype-note">Ranking and filters use midpoint estimates.</span>
</p>
<p>Course gross income: ${esc(money(r.courseIncome))} · Available course income: ${esc(money(r.budget))} · Average monthly burden: ${esc(money(r.monthly))}.</p>
<details class="debug">
<summary>Medical baseline, formulas, rates & treatment phases</summary>
<p>Fictional full-course baseline: <strong>${esc(money(r.baseline))}</strong>, the midpoint of ${esc(money(r.price.standard_charge_min))}–${esc(money(r.price.standard_charge_max))}. Source table: ${esc(r.price.source_table)}; package ID: ${esc(r.price.treatment_id)}; type: ${esc(r.price.treatment_type)}. All amounts are USD per full course.</p>
<p>${esc(r.med.assumption)} Deductible component: ${esc(money(r.med.deductible))}; coinsurance before cap: ${esc(money(r.med.coinsurance))}. Insured estimate = min(remaining cap, deductible + remaining baseline × coinsurance).</p>
<p>Travel: ${r.summary.visits} × 2 × ${esc(r.distance)} × ${r.mileage.cents_per_mile}¢. Overnight stays: ${esc(r.nights)}; nightly lodging ${money(r.lodging.lodging)} + meals ${money(r.lodging.meals)} (${r.lodging.county==='STANDARD'?'state fallback':'county rate'}). Childcare: ${money(r.care.weekly_price)} weekly / 5 × ${esc(current.profile.children)} × ${r.summary.visits} (${esc(r.care.county)}, ${r.care.study_year}${r.care.county==='STANDARD'?', median fallback':''}).</p>
<p>Lost wages: ${r.summary.visits} × ${esc(current.profile.missedHours)} hours × ${esc(money(current.profile.hourly))}. Income period: ${r.summary.weeks}/52 of annual income; monthly expenses use the same period.</p>${phaseTable(current.profile.regimen)}</details>
<h3 style="margin-top:18px">${aid.length} potential assistance matches${aidText?' after text filter':''}</h3>
<p class="small">Screened against diagnosis, known subtype, age, insurance, FPL and grouped residence/treatment geography. Additional requirements and funding availability need review. Awards are not subtracted from cost.</p>${aid.length?aid.map(aidCard).join(''):'<p>No potential assistance matches for this profile and assistance filter. See exclusions below.</p>'}<details class="debug">
<summary>${excluded.length} excluded assistance programs — reasons</summary>${excluded.map(aidCard).join('')}</details>
<details class="debug">
<summary>Full calculation record (debug)</summary>
<pre>${esc(JSON.stringify(r,null,2))}</pre>
</details>
</article>`;
 }).join('')+navigation();
 for(const button of $('results').querySelectorAll('[data-page]'))button.addEventListener('click',()=>{page=Number(button.dataset.page);render();$('results').scrollIntoView({block:'start'});});
}
function clearFilters(){for(const id of ['hospitalFilter','maxDistance','maxCost','aidType'])$(id).value='';$('eligibility').value='';$('sort').value='';page=1;render();}
async function initialize(){
 const [cancers,hospitals,counties,addresses,info]=await Promise.all([
  requestAPI('/api/cancers'),requestAPI('/api/hospitals'),requestAPI('/api/nc-counties'),
  requestAPI('/api/addresses'),requestAPI('/api/prototype-info')
 ]);
 DATA.cancer_type=cancers;DATA.hospital=hospitals;DATA.county=counties;HOSPITAL_IDS=info.hospitalIds;
 $('cancer').innerHTML=placeholder()+cancers.map(c=>option(c.cancer_id,c.name)).join('');
 $('location').innerHTML=placeholder()+addresses.map(a=>option(a.address_id,a.street_address+', '+a.city+', '+a.state+' ('+a.county+' County)')).join('');
 $('county').innerHTML=placeholder()+counties.map(county=>option(county,county)).join('');
 $('hospitalFilter').innerHTML+=hospitals.map(h=>option(h.hospital_id,h.name)).join('');
 $('distances').innerHTML=HOSPITAL_IDS.map(h=>`<label for="distance_${h}">${esc(hospitals.find(x=>x.hospital_id===h).name)}</label>
<input class="debug" id="distance_${h}" type="number" min="0" max="2000" step="0.1" required>`).join('');
 $('provenance').textContent=JSON.stringify(info,null,2);
 $('cancer').addEventListener('change',()=>updateRegimen().catch(showRequestError));
 $('regimen').addEventListener('change',()=>regimenInfo().catch(showRequestError));
 $('location').addEventListener('change',()=>setLocation().catch(showRequestError));
 const profileChanged=()=>{profileVersion++;updateConditionalFields();$('stale').hidden=!current;};
 $('profile').addEventListener('input',profileChanged);$('profile').addEventListener('change',profileChanged);
 $('profile').addEventListener('submit',e=>{e.preventDefault();if(!$('compareButton').disabled)run();});
 $('load').addEventListener('click',loadCase);
 for(const id of ['hospitalFilter','maxDistance','maxCost','eligibility','sort','aidType'])$(id).addEventListener('input',()=>{page=1;render();});
 $('clearFilters').addEventListener('click',clearFilters);$('regimen').innerHTML=placeholder();
 for(const id of ['cancer','regimen','location','state','county','insurance'])$(id).required=true;
 updateConditionalFields();$('runtimeStatus').hidden=true;setBusy(false);
}
initialize().catch(showStartupError);
