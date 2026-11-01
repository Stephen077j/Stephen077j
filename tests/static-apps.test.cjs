'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const applications = [
  { path: 'projects/taskflow-lite/index.html', ids: ['new-task', 'title', 'tasks', 'count', 'export-json'], title: 'TaskFlow Lite' },
  { path: 'projects/reposcope/index.html', ids: ['search', 'username', 'query', 'sort', 'grid', 'status'], title: 'RepoScope' }
];
for (const app of applications) {
  test(app.title + ': HTML entry point and required controls', () => {
    const html = fs.readFileSync(path.resolve(__dirname, '..', app.path), 'utf8');
    assert.match(html, /<!doctype html>/i);
    assert.match(html, /<meta name="viewport"/i);
    assert.match(html, /<title>[^<]+<\/title>/i);
    for (const id of app.ids) {
      assert.ok(html.includes('id="' + id + '"'), 'Missing control: ' + id);
    }
    const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)];
    assert.ok(scripts.length > 0, 'Expected inline JS');
    for (const [, script] of scripts) new vm.Script(script, { filename: app.path });
    assert.ok(html.includes('textContent'), 'Safe text rendering expected');
  });
  test(app.title + ': project documentation present', () => {
    const readme = fs.readFileSync(path.resolve(__dirname, '..',path.dirname(app.path),'README.md'), 'utf8');
    assert.match(readme, /^# /);
    assert.ok(readme.length > 200);
  });
}
test('TaskFlow: local-only state and backup export', () => {
  const source = fs.readFileSync(path.resolve(__dirname, '../projects/taskflow-lite/index.html'), 'utf8');
  assert.match(source, /localStorage/);
  assert.match(source, /JSON\.stringify/);
  assert.match(source, /createObjectURL/);
});
test('RepoScope: public API endpoint and no embedded credentials', () => {
  const source = fs.readFileSync(path.resolve(__dirname, '../projects/reposcope/index.html'), 'utf8');
  assert.match(source, /api\.github\.com\/users\//);
  assert.doesNotMatch(source, /gh[pousr]_[A-Za-z0-9_]{20,}/);
});
