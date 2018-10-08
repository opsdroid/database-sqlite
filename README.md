⚠️ *DEPRECATED* ⚠️ This database module is now built in to [opsdroid core](https://opsdroid.readthedocs.io/en/stable/databases/sqlite/). This repository only exists for backward compatibility and will be removed.

opsdroid database sqlite
========================

A database module for [opsdroid](https://github.com/opsdroid/opsdroid) to persist memory in a sqlite database.


## Requirements

None.

## Configuration

```yaml
databases:
  sqlite:
    file: "my_file.db"  # (optional) default "~/.opsdroid/sqlite.db"
    table: "my_table"  # (optional) default "opsdroid"
```
