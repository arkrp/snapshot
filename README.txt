snapshot
Hannah Nelson 2026

This is a simple snapshot testing tool. It lets you create tests from 'snapshots' of outputs. This allows you to quickly create tests of functionality which you already have!

It has 3 commands

ss - snapshot:
    runs all the tests! gives you are report if they work.
si - snap_inspect:
    runs "git diff" on a selected reference snapshot and the current snapshot
sr - snap_rereference:
    overwrite the reference with the current snapshot for a selected test.

This has two system dependencies:
cat
git
