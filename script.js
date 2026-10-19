const $ = (s, p=document) => p.querySelector(s);
const $$ = (s, p=document) => [...p.querySelectorAll(s)];

// Smooth, animated route transitions for the single-page portfolio.
const transition = $('.page-transition');
const navLinks = $$('.nav-links a');
const menu = $('.nav-links');
const menuToggle = $('.menu-toggle');

function setActive(id){
  navLinks.forEach(a => a.classList.toggle('active', a.dataset.route === id));
}

function routeTo(id, updateHash=true){
  const target = document.getElementById(id);
  if(!target) return;
  setActive(id);
  menu.classList.remove('open');
  document.body.classList.remove('menu-open');
  transition.classList.add('active');
  gsap.fromTo('.transition-grid',{scale:1.25,opacity:0},{scale:1,opacity:1,duration:.38,ease:'power2.out'});
  gsap.fromTo('.transition-label',{y:20,opacity:0},{y:0,opacity:1,duration:.28,delay:.08});
  setTimeout(()=>{
    const navH = document.getElementById('navbar')?.offsetHeight || 80;
    const top = target.getBoundingClientRect().top + window.scrollY - navH;
    window.scrollTo({top, behavior:'smooth'});
    setTimeout(()=>transition.classList.remove('active'),420);
  },240);
  if(updateHash) history.replaceState(null,'','#'+id);
}

$$('[data-route]').forEach(a=>a.addEventListener('click', e=>{e.preventDefault();routeTo(a.dataset.route)}));
menuToggle.addEventListener('click',()=>{menu.classList.toggle('open');document.body.classList.toggle('menu-open')});

// Auto-update nav active on scroll via IntersectionObserver
const sections = $$('.page-section[id]');
let scrollLock = false;
const navObserver = new IntersectionObserver(entries=>{
  if(scrollLock) return;
  entries.forEach(entry=>{
    if(entry.isIntersecting) setActive(entry.target.id);
  });
},{threshold:0.3});
sections.forEach(s=>navObserver.observe(s));

// Mouse effects. Humanity invented cursor trails, so here we are.
const dot=$('.cursor-dot'), ring=$('.cursor-ring');
window.addEventListener('pointermove',e=>{gsap.to(dot,{x:e.clientX,y:e.clientY,duration:.08});gsap.to(ring,{x:e.clientX,y:e.clientY,duration:.25,ease:'power2.out'})});
$$('a,button,.tilt-card,.skill-card').forEach(el=>{el.addEventListener('mouseenter',()=>ring.classList.add('hover'));el.addEventListener('mouseleave',()=>ring.classList.remove('hover'))});

// Magnetic buttons.
$$('.magnetic').forEach(el=>{
  el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect();gsap.to(el,{x:(e.clientX-r.left-r.width/2)*.12,y:(e.clientY-r.top-r.height/2)*.12,duration:.3})});
  el.addEventListener('pointerleave',()=>gsap.to(el,{x:0,y:0,duration:.5,ease:'elastic.out(1,.4)'}));
});

// 3D tilt cards.
$$('.tilt-card').forEach(card=>{
  card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();const rx=((e.clientY-r.top)/r.height-.5)*-8;const ry=((e.clientX-r.left)/r.width-.5)*10;gsap.to(card,{rotateX:rx,rotateY:ry,duration:.35,transformPerspective:900,ease:'power2.out'})});
  card.addEventListener('pointerleave',()=>gsap.to(card,{rotateX:0,rotateY:0,duration:.6,ease:'power3.out'}));
});

// Scroll progress.
window.addEventListener('scroll',()=>{const max=document.documentElement.scrollHeight-innerHeight;$('.scroll-progress span').style.width=(scrollY/max*100)+'%'});

// Three.js hero: wireframe torus + particles + floating nodes.
function initHero3D(){
  const mount=$('#three-hero'); if(!mount || !window.THREE) return;
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,100); camera.position.set(0,0,7);
  const renderer=new THREE.WebGLRenderer({alpha:true,antialias:true}); renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.setSize(innerWidth,innerHeight); mount.appendChild(renderer.domElement);
  const group=new THREE.Group(); scene.add(group); group.position.x=innerWidth<900?.9:1.55;
  const geo=new THREE.TorusKnotGeometry(1.45,.055,180,14,2,3);
  const mat=new THREE.MeshBasicMaterial({color:0x64f5ff,wireframe:true,transparent:true,opacity:.55});
  const knot=new THREE.Mesh(geo,mat); group.add(knot);
  const ringGeo=new THREE.TorusGeometry(2.2,.008,12,100); const ringMat=new THREE.MeshBasicMaterial({color:0x9c7cff,transparent:true,opacity:.4});
  const r1=new THREE.Mesh(ringGeo,ringMat);r1.rotation.x=.8;group.add(r1);const r2=r1.clone();r2.rotation.y=1.2;group.add(r2);
  const pGeo=new THREE.BufferGeometry(); const count=700; const pos=new Float32Array(count*3);
  for(let i=0;i<count*3;i++) pos[i]=(Math.random()-.5)*11;
  pGeo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  const pMat=new THREE.PointsMaterial({color:0x8ca8ff,size:.012,transparent:true,opacity:.65});scene.add(new THREE.Points(pGeo,pMat));
  let mx=0,my=0; window.addEventListener('pointermove',e=>{mx=(e.clientX/innerWidth-.5)*.5;my=(e.clientY/innerHeight-.5)*.5});
  function animate(){requestAnimationFrame(animate);knot.rotation.x+=.0018;knot.rotation.y+=.004;r1.rotation.z+=.002;r2.rotation.x-=.0015;group.rotation.y+=(mx-group.rotation.y)*.02;group.rotation.x+=((my*-0.3)-group.rotation.x)*.02;renderer.render(scene,camera)} animate();
  addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);group.position.x=innerWidth<900?.9:1.55});
}

// Contact particles.
function initContact3D(){
  const mount=$('#contact-canvas');if(!mount||!window.THREE)return;
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,100),renderer=new THREE.WebGLRenderer({alpha:true,antialias:true});
  camera.position.z=8;renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(innerWidth,innerHeight);mount.appendChild(renderer.domElement);
  const geo=new THREE.BufferGeometry(),count=380,arr=new Float32Array(count*3);for(let i=0;i<count;i++){arr[i*3]=(Math.random()-.5)*14;arr[i*3+1]=(Math.random()-.5)*8;arr[i*3+2]=(Math.random()-.5)*6}geo.setAttribute('position',new THREE.BufferAttribute(arr,3));
  const pts=new THREE.Points(geo,new THREE.PointsMaterial({color:0x9c7cff,size:.025,transparent:true,opacity:.75}));scene.add(pts);
  const ico=new THREE.IcosahedronGeometry(2.4,1),wire=new THREE.Mesh(ico,new THREE.MeshBasicMaterial({color:0x64f5ff,wireframe:true,transparent:true,opacity:.08}));scene.add(wire);
  function tick(){requestAnimationFrame(tick);pts.rotation.y+=.0006;wire.rotation.x+=.001;wire.rotation.y-=.0012;renderer.render(scene,camera)}tick();
  addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
}

// Project slideshow.
const slides=$$('.project-slide'), dots=$$('#slideDots button'), count=$('#slideCount');let current=0;
function showSlide(next){current=(next+slides.length)%slides.length;slides.forEach((s,i)=>s.classList.toggle('active',i===current));dots.forEach((d,i)=>d.classList.toggle('active',i===current));if(count) count.textContent=`${String(current+1).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}`}
$('#nextProject').addEventListener('click',()=>showSlide(current+1));$('#prevProject').addEventListener('click',()=>showSlide(current-1));dots.forEach((d,i)=>d.addEventListener('click',()=>showSlide(i)));
let slideTimer=setInterval(()=>showSlide(current+1),7000);$('#projectSlider').addEventListener('mouseenter',()=>clearInterval(slideTimer));$('#projectSlider').addEventListener('mouseleave',()=>slideTimer=setInterval(()=>showSlide(current+1),7000));

// Social Channels Modal & Discord Copy
const socialModal=$('#socialModal');
const openSocialsBtn=$('#openSocialsBtn');
const closeSocialModal=$('#closeSocialModal');
const copyDiscordChip=$('#copyDiscordChip');
const copyDiscordModalBtn=$('#copyDiscordModalBtn');
const discordChipBadge=$('#discordChipBadge');
const modalDiscordCopyBadge=$('#modalDiscordCopyBadge');
const modalToast=$('#modalToast');

function openModal(){if(socialModal){socialModal.classList.add('active');socialModal.setAttribute('aria-hidden','false')}}
function closeModal(){if(socialModal){socialModal.classList.remove('active');socialModal.setAttribute('aria-hidden','true')}}

if(openSocialsBtn) openSocialsBtn.addEventListener('click', openModal);
if(closeSocialModal) closeSocialModal.addEventListener('click', closeModal);
if(socialModal){
  socialModal.addEventListener('click',e=>{if(e.target===socialModal) closeModal()});
  window.addEventListener('keydown',e=>{if(e.key==='Escape'&&socialModal.classList.contains('active')) closeModal()});
}

function copyDiscordHandle(){
  const handle='vitocorleone0182';
  navigator.clipboard.writeText(handle).then(()=>{
    if(discordChipBadge) discordChipBadge.textContent='Copied! ✓';
    if(modalDiscordCopyBadge) modalDiscordCopyBadge.textContent='Copied! ✓';
    if(modalToast){
      modalToast.classList.add('show');
      setTimeout(()=>modalToast.classList.remove('show'),3000);
    }
    setTimeout(()=>{
      if(discordChipBadge) discordChipBadge.textContent='Copy';
      if(modalDiscordCopyBadge) modalDiscordCopyBadge.textContent='Copy';
    },2500);
  }).catch(()=>{
    prompt('Copy Discord username:', handle);
  });
}

if(copyDiscordChip) copyDiscordChip.addEventListener('click', copyDiscordHandle);
if(copyDiscordModalBtn) copyDiscordModalBtn.addEventListener('click', copyDiscordHandle);

// ==========================================
// Verified Certificates & Internships Lightbox Logic
// ==========================================
const internsData = [
  {
    type: 'INTERNSHIP CREDENTIAL',
    title: 'Python Project Intern Certificate',
    issuer: 'Cybernaut EdTech Private Limited',
    date: '10 Nov 2025 – 10 Feb 2026',
    id: 'CNPPI02500116',
    isGoogleBadge: false,
    img: 'intern_certificate/cybernaut_intern.png',
    directUrl: 'intern_certificate/cybernaut_intern.png',
    tags: ['Python Automation', 'Data Parsing', 'SIEM Log Preparation', 'Scripting', 'Quality Reporting'],
    desc: 'Official Certificate of Employment & Internship issued by Cybernaut EdTech Private Limited recognizing commendable performance and engineering contributions in Python project automation.'
  },
  {
    type: 'INTERNSHIP CREDENTIAL',
    title: 'Penetration Testing & Security Internship Certificate',
    issuer: 'Pargavan Cybber Solutions',
    date: '08 July 2025 – 28 July 2025',
    id: 'Paavai Engg / PCS-2025',
    isGoogleBadge: false,
    img: 'intern_certificate/pargavan_intern.png',
    directUrl: 'intern_certificate/pargavan_intern.png',
    tags: ['Penetration Testing', 'Linux Commands', 'Burp Suite', 'Target Footprinting', 'VAPT Report'],
    desc: '15-Day intensive practical industry program covering networking fundamentals, target footprinting, service exploitation, OWASP Top 10 attacks, and professional VAPT report delivery.'
  }
];

const certsData = [
  {
    type: 'PROFESSIONAL CERTIFICATION',
    title: 'Google Security Operations – SOAR Analyst',
    issuer: 'Google Cloud Skills Boost',
    date: 'Jul 2026',
    id: '25493233',
    isGoogleBadge: true,
    img: '',
    directUrl: 'https://www.skills.google/public_profiles/5804b14b-123b-4960-9b6c-35057b6d7b04/badges/25493233?utm_medium=social&utm_source=linkedin&utm_campaign=ql-social-share',
    tags: ['Google SecOps', 'SOAR Workflows', 'Incident Triage', 'Security Automation', 'Playbook Engineering'],
    desc: 'Official credential verifying proficiency in Google Security Operations (SecOps), automated playbook engineering, alert correlation, and incident response orchestration.'
  },
  {
    type: 'NATIONAL HACKATHON CREDENTIAL',
    title: 'Certificate of Participation – "OS – Bug Bounty Challenge"',
    issuer: 'C-DAC Chennai (Govt of India)',
    date: '7-8 July 2026',
    id: 'CDAC-CHE-BB26',
    isGoogleBadge: false,
    img: 'certificates/cdac_bug_bounty.jpg',
    directUrl: 'certificates/cdac_bug_bounty.jpg',
    tags: ['Bug Bounty', 'C-DAC Chennai', 'National Hackathon', 'OS Vulnerability', 'Exploit Analysis'],
    desc: 'National-Level 36-Hour Hackathon conducted by C-DAC Chennai, executing operating system vulnerability discovery, system-level bug hunting, and structured exploit reporting.'
  },
  {
    type: 'ACHIEVEMENT CERTIFICATION',
    title: 'Certificate of Achievement – Ethical Hacking & Cybersecurity',
    issuer: 'Hacker X',
    date: '12 July 2025',
    id: '513f84fabaf8111',
    isGoogleBadge: false,
    img: 'certificates/hackerx_ethical_hacking.jpg',
    directUrl: 'certificates/hackerx_ethical_hacking.jpg',
    tags: ['Ethical Hacking', 'VAPT', 'OWASP Top 10', 'Penetration Testing', 'Network Security'],
    desc: 'Certification of Achievement successfully passing examination in offensive security principles, network reconnaissance, web vulnerability exploitation, and security remediation.'
  },
  {
    type: 'TECHNICAL CERTIFICATION',
    title: 'Certificate of Completion – Introduction to API Pentesting & Bug Bounty 101',
    issuer: 'Cappriciosec University (MSME Certified)',
    date: '28 July 2025',
    id: '46315a0090e15e7ee9c6',
    isGoogleBadge: false,
    img: 'certificates/cappriciosec_api_pentesting.png',
    directUrl: 'certificates/cappriciosec_api_pentesting.png',
    tags: ['API Pentesting', 'Bug Bounty', 'Postman', 'Burp Suite', 'SQL Injection', 'OOB Testing'],
    desc: 'Certified completion of intensive program in API hacking, Postman, Burp Suite, out-of-band (OOB) testing, Python API development, CRUD operations, authentication/authorization bypasses, and command injection.'
  },
  {
    type: 'TECHNICAL SEMINAR CREDENTIAL',
    title: 'Seminar on Social Engineering & Ethical Hacking',
    issuer: 'Cappriciosec University (MSME Certified)',
    date: '08 August 2025',
    id: '7f8a9aed21666ac6b0d9',
    isGoogleBadge: false,
    img: 'certificates/cappriciosec_seminar.jpg',
    directUrl: 'certificates/cappriciosec_seminar.jpg',
    tags: ['Social Engineering', 'Keyloggers', 'SET Tool', 'Phishing Analysis', 'Ethical Hacking'],
    desc: 'Completion of intensive seminar covering social engineering vectors, prevention techniques, keylogger detection, advanced exploitation toolsets, and human-factor security.'
  }
];

const certModal = $('#certModal');
const closeCertModal = $('#closeCertModal');
const certModalTitle = $('#certModalTitle');
const certModalImg = $('#certModalImg');
const certBadgeFrame = $('#certBadgeFrame');
const certVisualToolbar = $('#certVisualToolbar');
const certModalDirectLink = $('#certModalDirectLink');
const certModalDownloadLink = $('#certModalDownloadLink');
const certModalIssuer = $('#certModalIssuer');
const certModalId = $('#certModalId');
const certModalDate = $('#certModalDate');
const certModalTags = $('#certModalTags');
const certModalDesc = $('#certModalDesc');
const prevCertBtn = $('#prevCertBtn');
const nextCertBtn = $('#nextCertBtn');
const certNavCounter = $('#certNavCounter');

let activeList = certsData;
let currentCertIdx = 0;

function renderCertModal(idx, list = activeList) {
  activeList = list;
  currentCertIdx = (idx + activeList.length) % activeList.length;
  const cert = activeList[currentCertIdx];
  if (!cert) return;

  if (certModalTitle) certModalTitle.textContent = cert.title;
  if (certModalIssuer) certModalIssuer.textContent = cert.issuer;
  if (certModalId) certModalId.textContent = cert.id;
  if (certModalDate) certModalDate.textContent = cert.date;
  if (certModalDesc) certModalDesc.textContent = cert.desc;
  if (certNavCounter) certNavCounter.textContent = `${String(currentCertIdx + 1).padStart(2, '0')} / ${String(activeList.length).padStart(2, '0')}`;

  if (certModalTags) {
    certModalTags.innerHTML = cert.tags.map(t => `<span>${t}</span>`).join('');
  }

  if (cert.isGoogleBadge) {
    if (certModalImg) certModalImg.style.display = 'none';
    if (certBadgeFrame) certBadgeFrame.style.display = 'flex';
    if (certVisualToolbar) certVisualToolbar.style.display = 'none';
  } else {
    if (certModalImg) {
      certModalImg.style.display = 'block';
      certModalImg.src = cert.img;
    }
    if (certBadgeFrame) certBadgeFrame.style.display = 'none';
    if (certVisualToolbar) certVisualToolbar.style.display = 'flex';
    if (certModalDirectLink) certModalDirectLink.href = cert.directUrl;
    if (certModalDownloadLink) certModalDownloadLink.href = cert.img;
  }
}

function openCertModalView(idx = 0, list = certsData) {
  renderCertModal(idx, list);
  if (certModal) {
    certModal.classList.add('active');
    certModal.setAttribute('aria-hidden', 'false');
  }
}

function closeCertModalView() {
  if (certModal) {
    certModal.classList.remove('active');
    certModal.setAttribute('aria-hidden', 'true');
  }
}

// Attach to Timeline Intern Certificate buttons
$$('.btn-timeline-cert').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const idx = parseInt(btn.dataset.internIdx, 10) || 0;
    openCertModalView(idx, internsData);
  });
});

// Attach to Certifications cards buttons
$$('.btn-cert-inspect').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const idx = parseInt(btn.dataset.certIdx, 10) || 0;
    openCertModalView(idx, certsData);
  });
});

$$('.cert-card').forEach(card => {
  card.addEventListener('click', (e) => {
    if (e.target.closest('a') || e.target.closest('button')) return;
    const idx = parseInt(card.dataset.certIndex, 10) || 0;
    openCertModalView(idx, certsData);
  });
});

if (closeCertModal) closeCertModal.addEventListener('click', closeCertModalView);
if (prevCertBtn) prevCertBtn.addEventListener('click', () => renderCertModal(currentCertIdx - 1, activeList));
if (nextCertBtn) nextCertBtn.addEventListener('click', () => renderCertModal(currentCertIdx + 1, activeList));

if (certModal) {
  certModal.addEventListener('click', e => {
    if (e.target === certModal) closeCertModalView();
  });
  window.addEventListener('keydown', e => {
    if (!certModal.classList.contains('active')) return;
    if (e.key === 'Escape') closeCertModalView();
    if (e.key === 'ArrowLeft') renderCertModal(currentCertIdx - 1, activeList);
    if (e.key === 'ArrowRight') renderCertModal(currentCertIdx + 1, activeList);
  });
}

// Scroll entrance animations.
gsap.registerPlugin(ScrollTrigger);
$$('.reveal').forEach(el=>{gsap.to(el,{opacity:1,y:0,duration:.85,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 88%',once:true}})});
$$('.skill-card').forEach((el,i)=>{gsap.fromTo(el,{y:35,opacity:0},{y:0,opacity:1,duration:.7,delay:i*.06,ease:'power3.out',scrollTrigger:{trigger:'.skills-grid',start:'top 80%',once:true}})});

initHero3D();initContact3D();
const initial=location.hash.replace('#','')||'home';setActive(document.getElementById(initial)?initial:'home');


