'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { linkedIssueNumbers, reviewPaths, replacedLabels, reconcile } = require('../scripts/review_lifecycle');

const path = 'reviews/2026/2026-11-17__big-team-science__v1.md';
const basePR = { number: 12, body: 'Closes #384', merged: false, head: { sha: 'head123' }, base: { ref: 'main', repo: { full_name: 'owner/repo' } } };
function setup({action='opened', pr={}, labels=['review:backlog','priority:high'], state='open', reason=null, checks=true, exists=true, files=[{filename:path,status:'added'}]}={}) {
  const calls = [];
  const issue = { number:384, state, state_reason:reason, labels:labels.map(name=>({name})) };
  const github = {
    paginate: async () => files,
    rest: {
      pulls: {listFiles:()=>{}},
      issues: {
        get: async()=>({data:issue}),
        setLabels: async({labels})=>{calls.push(['labels',labels]);issue.labels=labels.map(name=>({name}));},
        update: async(args)=>{calls.push(['update',args.state,args.state_reason]);issue.state=args.state;issue.state_reason=args.state_reason;},
      },
      checks: {listForRef:async()=>({data:{check_runs:checks?[
        {name:'index',status:'completed',conclusion:'success'},
        {name:'DCO / DCO',status:'completed',conclusion:'success'},
      ]:[{name:'index',status:'completed',conclusion:'failure'}]}})},
      repos: {getContent:async()=>exists?{data:{type:'file'}}:Promise.reject(Object.assign(new Error('missing'),{status:404}))},
    },
  };
  const context = {repo:{owner:'owner',repo:'repo'},payload:{action,pull_request:{...basePR,...pr},repository:{default_branch:'main'}}};
  return {github,context,calls,issue};
}

test('uses explicit local issue links only',()=>{
  assert.deepEqual(linkedIssueNumbers('Closes #384. Refs owner/repo#385. Fixes third-party/other#66. #12','owner','repo'),[384,385]);
});
test('recognizes only canonical review files',()=>{
  assert.deepEqual(reviewPaths([{filename:'README.md',status:'modified'},{filename:path,status:'added'}]),[path]);
});
test('preserves non-lifecycle labels',()=>{
  assert.deepEqual(replacedLabels(['review:backlog','priority:high'],'review:in-progress'),['priority:high','review:in-progress']);
});
test('opening a review PR applies in-progress',async()=>{
  const s=setup();assert.equal(await reconcile(s),'in-progress');
  assert.deepEqual(s.calls,[['labels',['priority:high','review:in-progress']]]);
});
test('repeated events produce no writes',async()=>{
  const s=setup({labels:['review:in-progress']});assert.equal(await reconcile(s),'in-progress');assert.equal(s.calls.length,0);
});
test('passing checks before merge does not publish',async()=>{
  const s=setup({labels:['review:in-progress']});assert.equal(await reconcile(s),'in-progress');assert.equal(s.issue.state,'open');
});
test('merged verified review is published and closed',async()=>{
  const s=setup({action:'closed',pr:{merged:true},labels:['review:in-progress','priority:high']});
  assert.equal(await reconcile(s),'published');
  assert.deepEqual(s.calls,[['labels',['priority:high','review:published']],['update','closed','completed']]);
});
test('previous GitHub issue auto-closure is idempotent',async()=>{
  const s=setup({action:'closed',pr:{merged:true},state:'closed',reason:'completed'});
  assert.equal(await reconcile(s),'published');assert.equal(s.calls.length,1);
});
test('failing checks prevent publication',async()=>{
  const s=setup({action:'closed',pr:{merged:true},checks:false});
  assert.equal(await reconcile(s),'required-checks-not-green');assert.equal(s.calls.length,0);
});
test('missing main-branch review prevents publication',async()=>{
  const s=setup({action:'closed',pr:{merged:true},exists:false});
  assert.equal(await reconcile(s),'review-not-on-main');assert.equal(s.calls.length,0);
});
test('closing without merging does not publish',async()=>{
  const s=setup({action:'closed'});assert.equal(await reconcile(s),'unmerged-pr');assert.equal(s.calls.length,0);
});
test('non-review PR does not change labels',async()=>{
  const s=setup({files:[{filename:'docs/guide.md',status:'modified'}]});
  assert.equal(await reconcile(s),'no-canonical-review-file');assert.equal(s.calls.length,0);
});
test('multiple issue references fail closed',async()=>{
  const s=setup({pr:{body:'Closes #384. Refs #390'}});
  assert.equal(await reconcile(s),'missing-or-ambiguous-issue-reference');assert.equal(s.calls.length,0);
});
test('editorial dispositions are respected',async()=>{
  const s=setup({labels:['disposition:declined'],state:'closed'});
  assert.equal(await reconcile(s),'not-admitted-to-review');assert.equal(s.calls.length,0);
});
test('delayed PR events cannot regress published issues',async()=>{
  const s=setup({labels:['review:published'],state:'closed',reason:'completed'});
  assert.equal(await reconcile(s),'terminal-issue');assert.equal(s.calls.length,0);
});
