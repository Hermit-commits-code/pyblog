---
title: Zero-Knowledge Journal
---

# Zero-Knowledge Journal (client-side encryption demo)

This page demonstrates encrypting and decrypting text entirely in the browser using the Web Crypto API. It also includes an example function to push encrypted blobs to GitHub via the REST API using a Personal Access Token kept in `localStorage` (do not hard-code tokens).

> Security notes:

- If you forget your master password, your data is permanently unrecoverable.
- Storing a GitHub token in `localStorage` has risks; only do this for personal use and rotate tokens frequently.

<div>
  <label>Master Password: <input id="zk-password" type="password" style="width:60%"/></label>
</div>
<div style="margin-top:8px">
  <textarea id="zk-plaintext" rows="8" style="width:100%" placeholder="Type your private note here..."></textarea>
</div>
<div style="margin-top:8px">
  <button id="encrypt">Encrypt & Show Blob</button>
  <button id="decrypt">Decrypt Blob</button>
  <button id="copyJson">Copy Encrypted JSON</button>
  <button id="saveGit">Save Encrypted File to GitHub</button>
</div>
<div style="margin-top:8px">
  <textarea id="zk-output" rows="8" style="width:100%" placeholder="Encrypted JSON will appear here"></textarea>
</div>

<script>
// Minimal zero-knowledge helpers using Web Crypto API (AES-GCM + PBKDF2)
function bufToB64(buf){return btoa(String.fromCharCode(...new Uint8Array(buf)))}
function b64ToBuf(b64){const s=atob(b64);const arr=new Uint8Array(s.length);for(let i=0;i<s.length;i++)arr[i]=s.charCodeAt(i);return arr.buffer}

async function deriveKey(password, salt){
  const pwUtf8 = new TextEncoder().encode(password);
  const baseKey = await crypto.subtle.importKey('raw', pwUtf8, 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey({name:'PBKDF2', salt, iterations:150_000, hash:'SHA-256'}, baseKey, {name:'AES-GCM', length:256}, false, ['encrypt','decrypt']);
}

async function encryptText(password, text){
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const key = await deriveKey(password, salt.buffer);
  const pt = new TextEncoder().encode(text);
  const ct = await crypto.subtle.encrypt({name:'AES-GCM', iv}, key, pt);
  return JSON.stringify({v:1, salt:bufToB64(salt), iv:bufToB64(iv), ct:bufToB64(ct)});
}

async function decryptJson(password, jsonStr){
  const obj = JSON.parse(jsonStr);
  const salt = b64ToBuf(obj.salt);
  const iv = b64ToBuf(obj.iv);
  const ct = b64ToBuf(obj.ct);
  const key = await deriveKey(password, salt);
  const pt = await crypto.subtle.decrypt({name:'AES-GCM', iv}, key, ct);
  return new TextDecoder().decode(pt);
}

// GitHub helper: store token in localStorage under 'gh_token'
async function saveToGitHub(path, contentBase64, message){
  const token = localStorage.getItem('gh_token');
  if(!token){throw new Error('No token found in localStorage. Set localStorage.setItem("gh_token", "ghp_...")')}
  const owner = 'Hermit-commits-code';
  const repo = 'pyblog';
  const url = `https://api.github.com/repos/${owner}/${repo}/contents/${encodeURIComponent(path)}`;
  // Try get existing to obtain sha for update
  const getResp = await fetch(url, { headers: { Authorization: 'token '+token, Accept:'application/vnd.github.v3+json' } });
  let body = { message, content: contentBase64 };
  if(getResp.ok){ const j = await getResp.json(); body.sha = j.sha }
  const resp = await fetch(url, { method:'PUT', headers:{ Authorization:'token '+token, Accept:'application/vnd.github.v3+json', 'Content-Type':'application/json' }, body: JSON.stringify(body) });
  if(!resp.ok) throw new Error('GitHub save failed: '+resp.status+' '+await resp.text());
  return resp.json();
}

document.getElementById('encrypt').onclick = async ()=>{
  try{
    const pw = document.getElementById('zk-password').value;
    const txt = document.getElementById('zk-plaintext').value;
    const json = await encryptText(pw, txt);
    document.getElementById('zk-output').value = json;
  }catch(e){alert('Encrypt error: '+e)}
}

document.getElementById('decrypt').onclick = async ()=>{
  try{
    const pw = document.getElementById('zk-password').value;
    const json = document.getElementById('zk-output').value;
    const pt = await decryptJson(pw, json);
    document.getElementById('zk-plaintext').value = pt;
  }catch(e){alert('Decrypt error: '+e)}
}

document.getElementById('copyJson').onclick = ()=>{
  navigator.clipboard.writeText(document.getElementById('zk-output').value);
}

document.getElementById('saveGit').onclick = async ()=>{
  try{
    const json = document.getElementById('zk-output').value;
    if(!json) return alert('No encrypted JSON to save');
    const blobName = `encrypted-journal/${new Date().toISOString().slice(0,10)}-${Math.random().toString(36).slice(2,8)}.json`;
    const contentBase64 = btoa(unescape(encodeURIComponent(json)));
    const res = await saveToGitHub(blobName, contentBase64, 'chore: add encrypted journal entry');
    alert('Saved to GitHub: '+res.content.path);
  }catch(e){alert('Save error: '+e)}
}
</script>
