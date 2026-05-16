#!/usr/bin/env node

/**
 * Node.js wrapper for create-context-graph Python CLI
 * 
 * To publish: npm publish --access public
 */

const { spawn } = require('child_process');
const path = require('path');

// Try to find uvx or fall back to pip
function findPythonRunner() {
  // First try uvx
  try {
    require('child_process').execSync('which uvx', { stdio: 'ignore' });
    return { runner: 'uvx', package: 'create-context-graph' };
  } catch (e) {
    // uvx not found, try pip installed version
    return { runner: 'python', package: '-m create_context_graph' };
  }
}

function run() {
  const { runner, package: pkg } = findPythonRunner();
  
  const child = spawn(runner, [pkg, ...process.argv.slice(2)], {
    stdio: 'inherit',
    shell: true
  });

  child.on('close', (code) => {
    process.exit(code);
  });

  child.on('error', (err) => {
    console.error('Error running create-context-graph:', err.message);
    console.error('\nPlease ensure uvx is installed: pip install uvx');
    process.exit(1);
  });
}

run();