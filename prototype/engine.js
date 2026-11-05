/* Calculations over embedded records, with explicit demo eligibility rules. */
const DEMO_DATE = '2026-11-04';
const HOSPITAL_IDS = ['DUKE','UNC','WFB','LEVINE','ECU'];
// Adult age cutoffs are fictional test rules, not admission policies.
const PROFILES = {DUKE:{minAge:18},UNC:{minAge:18},WFB:{minAge:21},LEVINE:{minAge:18},ECU:{minAge:18}};
const round = n => Math.round((n+Number.EPSILON)*100)/100;
const norm = s => String(s??'').trim().toLowerCase();
function validate(p) {
 const errors=[];
 for(const [key,min,max] of [['age',0,120],['size',1,20],['children',0,10],['income',0,1e9],['otherIncome',0,1e9],['expenses',0,1e7],['deductible',0,1e7],['cap',0,1e7],['coinsurance',0,100],['missedHours',0,24],['hourly',0,10000]]) {
  if(key==='hourly'&&!(p.missedHours>0)) continue;
  if(p.insurance==='Uninsured'&&['deductible','cap','coinsurance'].includes(key)) continue;
  if(!Number.isFinite(p[key])||p[key]<min||p[key]>max) errors.push(`${key} must be between ${min} and ${max}.`);
 }
 for(const key of ['age','size','children']) if(!Number.isInteger(p[key])) errors.push(`${key} must be a whole number.`);
 if(p.children>=p.size) errors.push('Children needing care must be fewer than household members (including the patient).');
 if(!DATA.cancer_type.some(c=>c.cancer_id===p.cancer)) errors.push('Select a supported diagnosis.');
 if(!DATA.regimen.some(r=>r.regimen_id===p.regimen&&r.cancer_id===p.cancer)) errors.push('Select a regimen for this diagnosis.');
 if(!['Private','Medicare','Medicaid','Uninsured'].includes(p.insurance)) errors.push('Select a supported insurance category.');
 if(p.state!=='NC') errors.push('This prototype supports North Carolina residents only.');
 if(p.children>0&&!['INFANT','TODDLER','PRESCHOOL','SCHOOL_AGE'].includes(p.ageGroup)) errors.push('Select a childcare age group.');
 if(!DATA.county.some(c=>c.county===p.county)) errors.push('Select an NC home county.');
 if(!p.address.trim()) errors.push('Enter an address or a fictional test address.');
 if(p.distances.some(n=>!Number.isFinite(n)||n<0||n>2000)||p.distances.length!==5) errors.push('Enter a one-way distance from 0 to 2,000 miles for every hospital.');
 if(p.insurance!=='Uninsured'&&p.deductible>p.cap) errors.push('Remaining deductible cannot exceed remaining out-of-pocket maximum.');
 return errors;
}
function finances(p) {
 const annual=p.income+p.otherIncome;
 const base=DATA.poverty_guideline.find(x=>x.year===2026&&x.region==='CONTIGUOUS'&&x.household_size===Math.min(8,p.size)).amount;
 const extra=DATA.poverty_guideline_extra.find(x=>x.region==='CONTIGUOUS').per_additional_person;
 const guideline=base+Math.max(0,p.size-8)*extra;
 return {annual,guideline,fpl:annual/guideline*100,monthly:annual/12,available:Math.max(0,annual/12-p.expenses)};
}
function medical(price,p) {
 if(p.insurance==='Uninsured') return {deductible:0,coinsurance:0,total:price,assumption:'Uninsured: full fictional baseline; no self-pay discount modeled.'};
 const deductible=Math.min(price,p.deductible);
 const coinsurance=Math.max(0,price-deductible)*p.coinsurance/100;
 return {deductible,coinsurance,total:round(Math.min(p.cap,deductible+coinsurance)),assumption:'All treatment assumed covered and in network. One remaining deductible and OOP cap across the entire course; no plan-year reset, premiums, copays, or uncovered services.'};
}
function geography(program,p,h) {
 const rules=DATA.assistance_program_geography.filter(r=>r.program_id===program.program_id);
 const groups=[...new Set(rules.map(r=>r.rule_group))];
 return groups.every(g=>rules.filter(r=>r.rule_group===g).some(r=>{
  const county=r.location_type==='treatment'?h.county:p.county;
  return r.country==='US'&&(!r.state||r.state==='NC')&&(!r.county||norm(r.county).replace(/ county$/,'')===norm(county));
 }));
}
function assistance(p,h,f) {
 const cancerNames={BREAST:'Breast',LUNG:'Lung',COLORECTAL:'Colorectal',PROSTATE:'Prostate',LYMPHOMA:'Lymphoma'};
 return DATA.assistance_program.map(a=>{
  const reasons=[],review=[];
  const cancers=DATA.assistance_program_cancer.filter(c=>c.program_id===a.program_id&&(c.cancer_type===cancerNames[p.cancer]||c.cancer_type==='Any'));
  if(!cancers.length) reasons.push('Diagnosis mismatch');
  else if(!cancers.some(c=>!c.cancer_subtype||norm(c.cancer_subtype)===norm(p.subtype))) {
   if(p.subtype) reasons.push('Subtype mismatch'); else review.push('Subtype required');
  }
  if(a.income_limit_fpl!=null&&f.fpl>a.income_limit_fpl) reasons.push(`Income exceeds ${a.income_limit_fpl}% FPL`);
  if(a.min_age!=null&&p.age<a.min_age||a.max_age!=null&&p.age>a.max_age) reasons.push('Age outside limits');
  const accepted=DATA.assistance_program_insurance.filter(i=>i.program_id===a.program_id).map(i=>norm(i.insurance_type));
  const insured=p.insurance!=='Uninsured';
  if(accepted.length&&!accepted.includes(norm(p.insurance))&&!(insured&&accepted.includes('any_insured'))&&!(['Medicare','Medicaid'].includes(p.insurance)&&accepted.includes('government insurance (unspecified)'))) reasons.push('Insurance mismatch');
  if(!insured&&norm(a.additional_insurance_requirements).includes('insurance must cover')) reasons.push('Insurance coverage required');
  if(!geography(a,p,h)) reasons.push('Residence or treatment geography mismatch');
  for(const key of ['other_eligibility_requirements','other_income_requirements','additional_insurance_requirements','notes']) if(a[key]) review.push(a[key]);
  return {...a,reasons,review,status:reasons.length?'Excluded':'Potential match — review required',geography_rules:DATA.assistance_program_geography.filter(r=>r.program_id===a.program_id),accepted_insurance:accepted};
 });
}
function search(p) {
 const errors=validate(p); if(errors.length) return {errors};
 const missing=DATA.hospital.filter(h=>!DATA.hospital_prices.some(x=>x.hospital_id===h.hospital_id&&x.cancer_id===p.cancer&&x.treatment_id===p.regimen));
 if(missing.length) return {errors:missing.map(h=>`Missing test price for ${h.name} / ${p.regimen}.`)};
 const f=finances(p), summary=DATA.summaries.find(r=>r.regimen_id===p.regimen);
 const mileage=DATA.mileage_rate.filter(r=>r.purpose==='MEDICAL'&&r.effective_date<=DEMO_DATE).sort((a,b)=>b.effective_date.localeCompare(a.effective_date))[0];
 const careRows=DATA.childcare_price.filter(c=>c.state==='NC'&&c.provider==='CENTER'&&c.age_group===(p.ageGroup||'PRESCHOOL'));
 const careYear=Math.max(...careRows.map(c=>c.study_year));
 const care=careRows.find(c=>c.study_year===careYear&&c.county===p.county)||careRows.find(c=>c.study_year===careYear&&c.county==='STANDARD');
 const results=DATA.hospital.map(h=>{
  const profile=PROFILES[h.hospital_id], distance=p.distances[HOSPITAL_IDS.indexOf(h.hospital_id)];
  const lodging=DATA.lodging_rate.find(l=>l.county===h.county&&l.fiscal_year===2027)||DATA.lodging_rate.find(l=>l.county==='STANDARD'&&l.fiscal_year===2027);
  const price=DATA.hospital_prices.find(x=>x.hospital_id===h.hospital_id&&x.cancer_id===p.cancer&&x.treatment_id===p.regimen);
  const baseline=round((price.standard_charge_min+price.standard_charge_max)/2), med=medical(baseline,p);
  const medicalMin=medical(price.standard_charge_min,p).total, medicalMax=medical(price.standard_charge_max,p).total;
  const nights=distance>=100?summary.visits:0;
  const costs={medical:med.total,travel:round(summary.visits*2*distance*mileage.cents_per_mile/100),lodging:nights*lodging.lodging,meals:nights*lodging.meals,childcare:round(summary.visits*p.children*care.weekly_price/5),lostWages:p.missedHours>0?round(summary.visits*p.missedHours*p.hourly):0};
  const total=round(Object.values(costs).reduce((a,b)=>a+b,0)), months=summary.weeks*12/52;
  const courseIncome=f.annual*summary.weeks/52, budget=f.available*months;
  const eligible=p.age>=profile.minAge;
  return {...h,eligible,eligibilityReason:eligible?`Passes fictional age rule (${profile.minAge}+); diagnosis offering assumed for demo. Clinical suitability and network status need confirmation.`:`Fails fictional adult program age rule (${profile.minAge}+).`,distance,price,baseline,med,medicalMin,medicalMax,costs,total,totalMin:round(total-med.total+medicalMin),totalMax:round(total-med.total+medicalMax),months,summary,nights,lodging,care,mileage,courseIncome,budget,gap:round(Math.max(0,total-budget)),burden:courseIncome>0?total/courseIncome*100:null,monthly:total/months,assistance:assistance(p,h,f)};
 }).sort((a,b)=>Number(b.eligible)-Number(a.eligible)||a.gap-b.gap||a.total-b.total||a.distance-b.distance);
 return {errors:[],profile:p,finances:f,results};
}
if(typeof module!=='undefined') module.exports={search,validate,finances,medical,assistance,HOSPITAL_IDS};
