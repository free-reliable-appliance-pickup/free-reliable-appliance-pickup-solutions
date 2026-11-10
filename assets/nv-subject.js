// Correct only outdated NV form email subjects inherited from an earlier template.
// Source page and state are checked; other state forms are never modified.
function correctNevadaFormSubjects(){
 document.querySelectorAll('form[action*="formspree.io"]').forEach(form=>{
  const source=form.querySelector('input[name="source_page"]')?.value||'';
  const subject=form.querySelector('input[name="_subject"]');
  if(!/^[a-z0-9-]+-nv-(?:appliance|washer-dryer|refrigerator|stove-oven|freezer)-pickup$/.test(source))return;
  if(subject&&/^UT /.test(subject.value))subject.value='NV '+subject.value.slice(3);
 });
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',correctNevadaFormSubjects,{once:true});
else correctNevadaFormSubjects();
document.addEventListener('submit',correctNevadaFormSubjects,true);
