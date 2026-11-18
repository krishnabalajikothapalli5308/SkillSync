import { useEffect, useState } from "react";
const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const starterSkills = "Python, FastAPI, SQL, React, Git";
export default function App() {
  const [token,setToken]=useState(localStorage.getItem("skillsync_token")||"");
  const [email,setEmail]=useState(""); const [password,setPassword]=useState("");
  const [authMode,setAuthMode]=useState("register");
  const [title,setTitle]=useState("Software Engineer Intern"); const [company,setCompany]=useState("HENNGE");
  const [description,setDescription]=useState(""); const [skills,setSkills]=useState(starterSkills);
  const [result,setResult]=useState(null); const [history,setHistory]=useState([]);
  const [cvResult,setCvResult]=useState(null); const [roadmap,setRoadmap]=useState([]);
  const [error,setError]=useState(""); const [loading,setLoading]=useState(false);
  async function api(path,options={}) {
    const headers={...(options.headers||{})}; if(token) headers.Authorization=`Bearer ${token}`;
    const response=await fetch(`${API}${path}`,{...options,headers});
    const data=await response.json().catch(()=>null);
    if(!response.ok) throw new Error(data?.detail||`Request failed (${response.status})`);
    return data;
  }
  async function authenticate(e) {
    e.preventDefault(); setError("");
    try {
      const path=authMode==="register"?"/api/auth/register":"/api/auth/login";
      const data=await api(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,password})});
      if(authMode==="register"){setAuthMode("login");setError("Account created. Sign in now.");}
      else {localStorage.setItem("skillsync_token",data.access_token);setToken(data.access_token);setPassword("");}
    } catch(err){setError(err.message);}
  }
  async function loadHistory(){if(!token)return;try{setHistory(await api("/api/analyses"));}catch(err){setError(err.message);}}
  useEffect(()=>{if(token)loadHistory();},[token]);
  async function analyze(e){
    e.preventDefault();setLoading(true);setError("");setResult(null);
    try{
      const data=await api("/api/analyses",{method:"POST",headers:{"Content-Type":"application/json"},
        body:JSON.stringify({title,company,description,current_skills:skills.split(",").map(s=>s.trim()).filter(Boolean)})});
      setResult(data);await loadHistory();
    }catch(err){setError(err.message);}finally{setLoading(false);}
  }
  async function uploadCV(e){
    const file=e.target.files?.[0];if(!file)return;setError("");setCvResult(null);
    const form=new FormData();form.append("file",file);
    try{setCvResult(await api("/api/cv/skills",{method:"POST",body:form}));}catch(err){setError(err.message);}
    e.target.value="";
  }
  async function generateRoadmap(){
    if(!result)return;
    try{const data=await api("/api/roadmaps",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({missing_skills:result.missing_skills})});setRoadmap(data.tasks);}
    catch(err){setError(err.message);}
  }
  function logout(){localStorage.removeItem("skillsync_token");setToken("");setResult(null);setHistory([]);setCvResult(null);setRoadmap([]);}
  return <main className="shell">
    <header className="topbar"><div className="brand"><span className="logo">S</span><span>SkillSync</span></div><div className="top-actions"><span className="tag">CAREER INTELLIGENCE</span>{token&&<button className="logout" onClick={logout}>Sign out</button>}</div></header>
    <section className="hero"><p className="eyebrow">CAREER CLARITY, BUILT WITH DATA</p><h1>Turn job descriptions<br/><em>into your next move.</em></h1><p className="sub">Understand what a role asks for, compare it with your current skills, and focus your learning where it matters.</p></section>
    {!token?<section className="auth-wrap"><form className="panel auth-panel" onSubmit={authenticate}><div className="panel-head"><div><p className="eyebrow">ACCOUNT</p><h2>{authMode==="register"?"Create your account":"Welcome back"}</h2></div></div>
      <label>Email<input type="email" value={email} onChange={e=>setEmail(e.target.value)} required/></label>
      <label>Password<input type="password" minLength="10" value={password} onChange={e=>setPassword(e.target.value)} required/></label>
      <button>{authMode==="register"?"Create account":"Sign in"} <span>↗</span></button>
      <p className="switch-auth">{authMode==="register"?"Already registered?":"New to SkillSync?"}<button type="button" className="text-button" onClick={()=>{setAuthMode(authMode==="register"?"login":"register");setError("");}}>{authMode==="register"?"Sign in":"Create an account"}</button></p>{error&&<p className="error">{error}</p>}
    </form></section>:<>
      <section className="utility-grid">
        <div className="panel utility-panel"><p className="eyebrow">PROFILE / CV</p><h2>Extract skills from your CV</h2><p className="utility-copy">Upload a text-based PDF or DOCX (maximum 5 MB). Files are processed in memory, not stored.</p>
          <label className="upload-label">Choose CV file<input type="file" accept=".pdf,.docx" onChange={uploadCV}/></label>
          {cvResult&&<div className="cv-result"><b>{cvResult.filename}</b><small>{cvResult.text_characters} characters scanned</small><div className="chips">{cvResult.extracted_skills.map(s=><span className="chip good" key={s}>{s}</span>)}</div><button className="secondary" type="button" onClick={()=>setSkills(cvResult.extracted_skills.join(", "))}>Use extracted skills</button></div>}
        </div>
        <div className="panel utility-panel"><p className="eyebrow">YOUR WORKSPACE</p><h2>Private analysis history</h2><p className="utility-copy">Saved job analyses belong to your account.</p><div className="stat"><strong>{history.length}</strong><span>recent analyses</span></div></div>
      </section>
      <section className="workspace"><form className="panel form-panel" onSubmit={analyze}>
        <div className="panel-head"><div><p className="eyebrow">01 / INPUT</p><h2>Analyze a role</h2></div><span className="step">LIVE ANALYSIS</span></div>
        <label>Job title<input value={title} onChange={e=>setTitle(e.target.value)} required/></label>
        <label>Company<input value={company} onChange={e=>setCompany(e.target.value)}/></label>
        <label>Job description<textarea value={description} onChange={e=>setDescription(e.target.value)} placeholder="Paste the job description here..." minLength={30} required/></label>
        <label>Your current skills <small>Comma-separated</small><textarea className="skills" value={skills} onChange={e=>setSkills(e.target.value)}/></label>
        <button disabled={loading}>{loading?"Analyzing...":"Analyze skill gap"} <span>↗</span></button>{error&&<p className="error">{error}</p>}<p className="disclaimer">Keyword-based baseline analysis, not a hiring decision.</p>
      </form>
      <section className="panel result-panel"><div className="panel-head"><div><p className="eyebrow">02 / INSIGHTS</p><h2>Your skill report</h2></div><span className="spark">✳</span></div>
        {!result?<div className="empty"><div className="empty-icon">◎</div><h3>Your analysis will appear here</h3><p>Paste a job description and run the analysis to see matched skills and gaps.</p></div>:<>
          <div className="score-row"><div><span className="muted">SKILL MATCH</span><div className="score">{result.match_score}<small>%</small></div></div><div className="score-note">{result.matched_skills.length} of {result.extracted_skills.length} detected skills matched.</div></div>
          <div className="meter"><span style={{width:`${result.match_score}%`}}/></div>
          <div className="skill-section"><h3>Matched skills <b className="green">{result.matched_skills.length}</b></h3><div className="chips">{result.matched_skills.map(s=><span className="chip good" key={s}>{s}</span>)}</div></div>
          <div className="skill-section"><h3>Skills to develop <b className="orange">{result.missing_skills.length}</b></h3><div className="chips">{result.missing_skills.map(s=><span className="chip gap" key={s}>{s}</span>)}</div></div>
          <button type="button" className="secondary" onClick={generateRoadmap}>Generate learning roadmap ↗</button>
          {roadmap.length>0&&<div className="roadmap">{roadmap.map((task,i)=><article key={task.skill}><b>{i+1}. {task.skill}</b><p>{task.objective}</p><small>Project: {task.suggested_project}</small><small>Proof: {task.verification}</small></article>)}</div>}
        </>}
      </section></section>
      <section className="history"><div className="panel-head"><div><p className="eyebrow">03 / TRACKING</p><h2>Recent analyses</h2></div><button className="refresh" onClick={loadHistory}>Refresh ↻</button></div>
        {history.length?<div className="history-list">{history.map(item=><div className="history-item" key={item.id}><div><b>{item.title}</b><small>{item.company||"Company not specified"} · {new Date(item.created_at).toLocaleDateString()}</small></div><strong>{item.match_score}%</strong></div>)}</div>:<p className="muted">No saved analyses yet.</p>}
      </section>
    </>}
    <footer><span>SKILLSYNC · PORTFOLIO PROJECT</span><span>Built for thoughtful career growth.</span></footer>
  </main>;
}
