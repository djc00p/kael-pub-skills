---
name: rubocop-performance
description: Fix RuboCop Performance violations in Rails and Ruby code. Understand why each cop matters, learn Rails-specific patterns (ActiveRecord queries, Enumerable chains, string operations), recognize autocorrectable offenses, and configure rubocop-performance in .rubocop.yml. Trigger on "RuboCop Performance", "Performance/", performance violations, or code reviews flagging perf issues.
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[],"env":[]},"os":["darwin","linux"]}}
---

# RuboCop Performance Cops — Rails Edition

RuboCop Performance catches code patterns that are slower than necessary. This skill teaches you _why_ each violation matters and how to fix it in Rails apps.

## Quick Start

**Enable rubocop-performance in your project:**

```yaml
# .rubocop.yml
require:
  - rubocop-performance

Performance:
  Enabled: true
```

Run `bundle exec rubocop` to scan your codebase. Most violations can be autocorrected with `--auto-correct` or `--auto-correct-all`.

**After any code review that identifies Performance violations, always close with:**
```bash
bundle exec rubocop --auto-correct-all
# Review the diff before committing — confirm no unintended changes
git diff
```
This catches all autocorrectable violations at once rather than fixing them one by one. For violations that require manual fixes (N+1 queries, load-order issues), note them explicitly as TODO items in the review response.

---

## Top Rails-Relevant Cops

### Performance/Count (Enabled by default)
**What it flags:** `Model.select { ... }.size` or similar chained operations on Enumerable.

**Why it matters:** Each intermediate method (`select`, `reject`, `find_all`) creates a new array. Combining logic into a single `count` method avoids temporary allocations.

**Rails context:** `Model.where(...).select { |m| m.active? }.count` is inefficient — use `Model.where(...).count { |m| m.active? }` or push conditions into the query.

**Fix pattern:**
```ruby
# bad
[1, 2, 3].select { |e| e > 2 }.size
Model.where(status: 'active').select { |m| m.valid? }.count

# good
[1, 2, 3].count { |e| e > 2 }
Model.where(status: 'active').to_a.count { |m| m.valid? }  # For ActiveRecord
```

**Autocorrect:** Yes (unsafe for ActiveRecord < 5.1).

---

### Performance/Size (Enabled by default)
**What it flags:** `.count` on arrays/hashes when `.size` is faster.

**Why it matters:** `Array#count` iterates over every element by default (O(n)). `Array#size` is O(1) — it just returns the internal length.

**Rails context:** Rails models use `.count` in queries (SQL), but on in-memory arrays, prefer `.size`.

**Fix pattern:**
```ruby
# bad
[1, 2, 3].count
{ a: 1, b: 2 }.count
records.to_a.count

# good
[1, 2, 3].size
{ a: 1, b: 2 }.size
records.to_a.size
```

**Autocorrect:** Yes.

---

### Performance/InefficientHashSearch (Disabled by default)
**What it flags:** `hash.keys.include?(key)` or `hash.values.include?(value)`.

**Why it matters:** `hash.keys` allocates a new array and then O(n)-searches it. `hash.key?` is O(1) hash lookup.

**Rails context:** Common when checking associations or caching logic.

**Fix pattern:**
```ruby
# bad
VALID_ROLES = { admin: 1, user: 2, guest: 3 }
VALID_ROLES.keys.include?(role)

# good
VALID_ROLES.key?(role)
VALID_ROLES.has_key?(role)  # alias
```

**Autocorrect:** Yes. Enable in `.rubocop.yml`:
```yaml
Performance/InefficientHashSearch:
  Enabled: true
```

---

### Performance/RegexpMatch (Enabled by default)
**What it flags:** `str.match(/regex/)` or `=~` when you only need a boolean.

**Why it matters:** `match` creates a `MatchData` object. `match?` is faster — it returns true/false without allocating.

**Rails context:** Validation patterns, string checks in callbacks.

**Fix pattern:**
```ruby
# bad
if user.email.match(/\A[\w]+@example\.com\z/)
  do_something
end

# bad
return if string =~ /pattern/

# good
if user.email.match?(/\A[\w]+@example\.com\z/)
  do_something
end

# good
return if string.match?(/pattern/)
```

**Autocorrect:** Yes.

---

### Performance/CompareWithBlock (Enabled by default)
**What it flags:** `array.sort { |a, b| a.foo <=> b.foo }`.

**Why it matters:** Blocks create overhead. `sort_by` is faster and cleaner — it pre-extracts values once, then sorts.

**Rails context:** Sorting nested objects, active records by an attribute.

**Fix pattern:**
```ruby
# bad
@users.sort { |a, b| a.created_at <=> b.created_at }
items.max { |a, b| a.priority <=> b.priority }

# good
@users.sort_by(&:created_at)
items.max_by(&:priority)
items.min_by(&:priority)
```

**Autocorrect:** Yes.

---

### Performance/FlatMap (Enabled by default)
**What it flags:** `array.map { ... }.flatten(1)`.

**Why it matters:** Two passes + intermediate array. `flat_map` combines map and flatten in one pass.

**Rails context:** Querying nested collections or plucking related records.

**Fix pattern:**
```ruby
# bad
@users.map { |u| u.posts }.flatten

# good
@users.flat_map { |u| u.posts }
```

**Autocorrect:** Yes.

---

### Performance/ReverseEach (Enabled by default)
**What it flags:** `array.reverse.each { ... }`.

**Why it matters:** `reverse` allocates a new array. `reverse_each` iterates backward without allocation.

**Rails context:** Iterating from newest to oldest (e.g., timestamps).

**Fix pattern:**
```ruby
# bad
@posts.reverse.each { |post| puts post.title }

# good
@posts.reverse_each { |post| puts post.title }
```

**Autocorrect:** Yes.

---

### Performance/StringReplacement (Enabled by default)
**What it flags:** `'abc'.gsub('b', 'd')` — single-char or simple replacements.

**Why it matters:** `gsub` with regex is overkill for literal strings. `tr` is faster for char-to-char swaps. `delete` for removals.

**Rails context:** Text sanitization, slug generation.

**Fix pattern:**
```ruby
# bad
'hello world'.gsub(' ', '-')
'test@example.com'.gsub('_', '.')

# good
'hello world'.tr(' ', '-')
'test@example.com'.tr('_', '.')

# bad
'hello world'.gsub(' ', '')

# good
'hello world'.delete(' ')
```

**Autocorrect:** Yes.

---

### Performance/DeletePrefix / DeleteSuffix (Requires Ruby 2.5+)
**What it flags:** `str.gsub(/\Aprefix/, '')` or `str.gsub(/suffix\z/, '')`.

**Why it matters:** Regex overhead for simple string trimming. `delete_prefix` and `delete_suffix` are dedicated methods (faster).

**Rails context:** Removing protocol from URLs, file extension stripping.

**Fix pattern:**
```ruby
# bad
url.gsub(/\Ahttps?:\/\//, '')
filename.gsub(/\.txt\z/, '')

# good
url.delete_prefix('https://')
url.delete_prefix('http://')
filename.delete_suffix('.txt')
```

**Autocorrect:** Yes (unsafe for `Pathname` objects).

---

### Performance/Detect (Enabled by default)
**What it flags:** `array.select { ... }.first` or `array.filter { ... }.last`.

**Why it matters:** `select` returns an array, then you pluck one element. `detect` returns the first match directly.

**Rails context:** Finding the first record matching a condition.

**Fix pattern:**
```ruby
# bad
@users.select { |u| u.premium? }.first
@users.filter { |u| u.active? }.last

# good
@users.detect { |u| u.premium? }
@users.reverse.detect { |u| u.active? }  # for last
```

**Autocorrect:** Yes (unsafe for non-Array receivers).

---

### Performance/FixedSize (Enabled by default)
**What it flags:** `'string'.size` or `[1, 2, 3].count` on literals.

**Why it matters:** You're calling a method on a static value that's known at parse time.

**Rails context:** Rare in app code, but catches test data and constants.

**Fix pattern:**
```ruby
# bad
raise StandardError, "Error" if message.length > 255

# good (but unusual)
raise StandardError, "Error" if message.length > 255  # OK on variable
```

**Autocorrect:** No, but RuboCop flags static literals.

---

### Performance/RedundantBlockCall (Enabled by default)
**What it flags:** `def method(&block); block.call; end`.

**Why it matters:** `block.call` creates a wrapper object. `yield` is faster.

**Rails context:** Custom iterators, callbacks.

**Fix pattern:**
```ruby
# bad
def map_records(&block)
  records.map { |r| block.call(r) }
end

# good
def map_records
  records.map { |r| yield(r) }
end
```

**Autocorrect:** Yes.

---

## Configuration

Add to `.rubocop.yml` to enable disabled-by-default cops or set severity:

```yaml
require:
  - rubocop-performance

Performance:
  Enabled: true

Performance/InefficientHashSearch:
  Enabled: true

Performance/Casecmp:
  Enabled: true

Performance/Count:
  Enabled: true
  Safe: false  # Unsafe for some ActiveRecord versions

Performance/OpenStruct:
  Enabled: true

# Exclude specific files or cops
Performance/Count:
  Exclude:
    - spec/**/*
    - lib/legacy.rb
```

---

## Working with ActiveRecord

**Key caveat:** Some cops are unsafe for ActiveRecord:

- **Performance/Count** — Rails < 5.1 ignores block passed to `count`. Use `Model.where(...).to_a.count { ... }` or push logic to the query.
- **Performance/Size** — `ActiveRecord::Relation#size` already does the smart thing (uses `count` if result not loaded, `length` if loaded).

**Rails-safe patterns:**

```ruby
# Good
User.where(status: 'active').size       # Knows to use SQL
User.where(status: 'active').length     # Always loads into memory

# Bad for perf, but safe
User.where(status: 'active').to_a.count { |u| u.premium? }

# Better
User.where(status: 'active', premium: true).count
```

---

## Ontology Hooks

When you fix a RuboCop Performance violation, log it to the shared knowledge graph:

**After fixing a violation:**
```bash
ont create --type Learning \
  --id learn_perf-$(date +%s) \
  --props '{"name":"rubocop-perf-fix","status":"complete","goal":"Fixed Performance/Count in app/models/user.rb: replaced select{}.size with count{}"}'
```

**If you spot a recurring pattern:**
```bash
ont create --type Learning \
  --id learn_perf-pattern-$(date +%s) \
  --props '{"name":"perf-pattern","status":"active","goal":"Recurring .select{}.count pattern in ActiveRecord queries — consider standardizing on .where().count or query methods"}'
```

---

## Full Cop Reference

See `references/cops.md` for detailed documentation of all RuboCop Performance cops, including disabled-by-default, unsafe, and rarely-used cops.

---

## Quick Links

- [RuboCop Performance Documentation](https://docs.rubocop.org/rubocop-performance/latest/)
- [Rails Performance Guide](https://guides.rubyonrails.org/performance_testing.html)
- [Ruby Best Practices](https://ruby-doc.org/)
