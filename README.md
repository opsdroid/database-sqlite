opsdroid database sqlite
========================

A database module for [opsdroid](https://github.com/opsdroid/opsdroid) to persist memory in a sqlite database.


## Requirements

None.

## Configuration

```yaml
databases:
  sqlite:
    file: "my_file.db"  # (optional) default "sqlite.db"
    table: "my_table"  # (optional) default "opsdroid"
```
