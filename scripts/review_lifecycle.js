'use strict';

// Trusted workflow only. PR head code is never checked out or executed.
const LIFECYCLE = new Set([
  'radar:candidate', 'radar:needs-judgment', 'review:backlog',
  'review:in-progress', 'review:published', 'disposition:deferred', 'disposition:declined',
]);
const ELIGIBLE = new Set(['review:backlog', 'review:in-progress', 'review:published']);
const REQUIRED_CHECKS = ['index', 'DCO / DCO'];
const REVIEW_FILE = /^reviews\/\d{4}\/\d{4}-\d{2}-\d{2}__[a-z0-9]+(?:-[a-z0-9]+)*__v\d+\.md$/;

function linkedIssueNumbers(body, owner, repo) {
  const numbers = new Set();
  const pattern = /\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?|refs?|review(?:s|ing)?)\s+(?:(?<remote>[\w.-]+\/[\w.-]+)#|#)(?<number>\d+)\b/gi;
  for (const match of (body || '').matchAll(pattern)) {
    if (match.groups.remote && match.groups.remote.toLowerCase() !== `${owner}/${repo}`.toLowerCase()) continue;
    numbers.add(Number(match.groups.number));
  }
  return [...numbers];
}

function reviewPaths(files) {
  return files.filter(file =>
    REVIEW_FILE.test(file.filename) && ['added', 'modified', 'renamed'].includes(file.status)
  ).map(file => file.filename);
}

function replacedLabels(labels, desired) {
  return [...new Set([...labels.filter(label => !LIFECYCLE.has(label)), desired])].sort();
}

function sameLabels(left, right) {
  const a = [...left].sort();
  const b = [...right].sort();
  return a.length === b.length && a.every((label, i) => label === b[i]);
}

async function checksPassed(github, owner, repo, sha) {
  const response = await github.rest.checks.listForRef({
    owner, repo, ref: sha, per_page: 100, filter: 'latest',
  });
  return REQUIRED_CHECKS.every(name => response.data.check_runs.some(check =>
    check.name === name && check.status === 'completed' && check.conclusion === 'success'
  ));
}

async function archived(github, owner, repo, paths, defaultBranch) {
  for (const path of paths) {
    try {
      const response = await github.rest.repos.getContent({ owner, repo, path, ref: defaultBranch });
      if (response.data.type === 'file') return true;
    } catch (error) {
      if (error.status !== 404) throw error;
    }
  }
  return false;
}

async function reconcile({ github, context }) {
  const { owner, repo } = context.repo;
  const pr = context.payload.pull_request;
  if (!pr || pr.base.repo.full_name.toLowerCase() !== `${owner}/${repo}`.toLowerCase()) return 'unrelated-repository';
  if (pr.base.ref !== context.payload.repository.default_branch) return 'non-default-branch';

  const numbers = linkedIssueNumbers(pr.body, owner, repo);
  if (numbers.length !== 1) return 'missing-or-ambiguous-issue-reference';
  const issue_number = numbers[0];
  const changed = await github.paginate(github.rest.pulls.listFiles, { owner, repo, pull_number: pr.number, per_page: 100 });
  const paths = reviewPaths(changed);
  if (!paths.length) return 'no-canonical-review-file';

  const issue = (await github.rest.issues.get({ owner, repo, issue_number })).data;
  if (issue.pull_request) return 'reference-is-a-pull-request';
  const labels = issue.labels.map(item => typeof item === 'string' ? item : item.name);
  if (!labels.some(label => ELIGIBLE.has(label))) return 'not-admitted-to-review';
  if (labels.includes('disposition:deferred') || labels.includes('disposition:declined')) return 'editorial-disposition';

  if (pr.merged && context.payload.action === 'closed') {
    if (!await checksPassed(github, owner, repo, pr.head.sha)) return 'required-checks-not-green';
    if (!await archived(github, owner, repo, paths, context.payload.repository.default_branch)) return 'review-not-on-main';
    const desired = replacedLabels(labels, 'review:published');
    if (!sameLabels(labels, desired)) {
      await github.rest.issues.setLabels({ owner, repo, issue_number, labels: desired });
    }
    if (issue.state !== 'closed' || issue.state_reason !== 'completed') {
      await github.rest.issues.update({ owner, repo, issue_number, state: 'closed', state_reason: 'completed' });
    }
    return 'published';
  }
  if (context.payload.action === 'closed') return 'unmerged-pr';
  if (issue.state !== 'open' || labels.includes('review:published')) return 'terminal-issue';
  const desired = replacedLabels(labels, 'review:in-progress');
  if (!sameLabels(labels, desired)) {
    await github.rest.issues.setLabels({ owner, repo, issue_number, labels: desired });
  }
  return 'in-progress';
}

module.exports = { linkedIssueNumbers, reviewPaths, replacedLabels, checksPassed, reconcile };
