# RuboCop Performance Cops — Complete Reference

Full documentation of all Performance cops. Status, safety, and autocorrect support included.

---

## Enabled by Default

### Performance/BindCall (Ruby 2.7+)
- **Autocorrect:** Yes (Safe)
- **Flags:** `umethod.bind(obj).call(args)` → `bind_call(obj, args)`
- **Why:** `bind_call` is faster; avoids intermediate object allocation.

### Performance/Caller
- **Autocorrect:** Yes (Safe)
- **Flags:** `caller[1]` → `caller(2..2).first`
- **Why:** Avoids full array allocation when you only need one frame.

### Performance/CompareWithBlock
- **Autocorrect:** Yes (Safe)
- **Flags:** `sort { |a, b| a.foo <=> b.foo }` → `sort_by(&:foo)`
- **Why:** `sort_by` is faster; pre-extracts values in one pass.

### Performance/Count
- **Autocorrect:** Yes (Unsafe for Rails < 5.1)
- **Flags:** `array.select { ... }.size` → `array.count { ... }`
- **Why:** Avoids intermediate array allocation.
- **Rails note:** Check Rails version before enabling for ActiveRecord.

### Performance/DeletePrefix (Ruby 2.5+)
- **Autocorrect:** Yes (Unsafe for Pathname)
- **Flags:** `str.gsub(/\Aprefix/, '')` → `str.delete_prefix('prefix')`
- **Why:** Dedicated method is faster than regex.

### Performance/DeleteSuffix (Ruby 2.5+)
- **Autocorrect:** Yes (Unsafe for Pathname)
- **Flags:** `str.gsub(/suffix\z/, '')` → `str.delete_suffix('suffix')`
- **Why:** Dedicated method is faster than regex.

### Performance/Detect
- **Autocorrect:** Yes (Unsafe for non-Array receivers)
- **Flags:** `array.select { ... }.first` → `array.detect { ... }`
- **Why:** Avoids creating intermediate array.

### Performance/DoubleStartEndWith
- **Autocorrect:** Yes (Safe)
- **Flags:** `str.start_with?("a") || str.start_with?("b")` → `str.start_with?("a", "b")`
- **Why:** Single method call is faster than branching.
- **Option:** `IncludeActiveSupportAliases` (include Rails `starts_with?`/`ends_with?`).

### Performance/EndWith
- **Autocorrect:** Yes (Unsafe for multiline strings)
- **Flags:** `'abc'.match?(/bc\Z/)` → `'abc'.end_with?('bc')`
- **Why:** Dedicated method avoids regex overhead.
- **Option:** `SafeMultiline: true` (default; don't flag `suffix$`).

### Performance/FixedSize
- **Autocorrect:** No
- **Flags:** `'string'.size` (literal)
- **Why:** Calling method on static value known at parse time.

### Performance/FlatMap
- **Autocorrect:** Yes (Safe)
- **Flags:** `array.map { ... }.flatten(1)` → `array.flat_map { ... }`
- **Why:** Single-pass operation; avoids intermediate array.

### Performance/RedundantBlockCall
- **Autocorrect:** Yes (Safe)
- **Flags:** `def foo(&block); block.call; end` → `def foo; yield; end`
- **Why:** `yield` is faster; no wrapper object.

### Performance/RedundantMatch
- **Autocorrect:** Yes (Safe)
- **Flags:** `str.match(/regex/)` (in boolean context) → `str.match?(/regex/)`
- **Why:** `match?` returns true/false without `MatchData` allocation.

### Performance/RegexpMatch
- **Autocorrect:** Yes (Safe)
- **Flags:** `str =~ /regex/` (in boolean context) → `str.match?(/regex/)`
- **Why:** `match?` is faster; no `MatchData` object created.

### Performance/ReverseEach
- **Autocorrect:** Yes (Safe)
- **Flags:** `array.reverse.each { ... }` → `array.reverse_each { ... }`
- **Why:** `reverse_each` iterates backward without allocating new array.

### Performance/Size
- **Autocorrect:** Yes (Safe)
- **Flags:** `[1, 2, 3].count` → `[1, 2, 3].size`
- **Why:** `size` is O(1); `count` is O(n).

### Performance/StartWith
- **Autocorrect:** Yes (Unsafe for multiline strings)
- **Flags:** `'abc'.match?(/\Aab/)` → `'abc'.start_with?('ab')`
- **Why:** Dedicated method avoids regex overhead.
- **Option:** `SafeMultiline: true` (default; don't flag `^start`).

### Performance/StringReplacement
- **Autocorrect:** Yes (Safe)
- **Flags:** `'abc'.gsub('b', 'd')` → `'abc'.tr('b', 'd')`
- **Why:** `tr` is faster for single-char replacements; `delete` for removals.

### Performance/StringIdentifierArgument
- **Autocorrect:** Yes (Safe)
- **Flags:** `send('method')` → `send(:method)`
- **Why:** Symbol avoids internal string-to-symbol conversion.

### Performance/TimesMap
- **Autocorrect:** Yes (Unsafe if count ≤ 0)
- **Flags:** `9.times.map { |i| ... }` → `Array.new(9) { |i| ... }`
- **Why:** Avoids creating enumerator object.

### Performance/UriDefaultParser
- **Autocorrect:** Yes (Safe)
- **Flags:** `URI::Parser.new` → `URI::DEFAULT_PARSER`
- **Why:** Reuses singleton; avoids instantiation overhead.

---

## Disabled by Default (Enable Explicitly)

### Performance/BigDecimalWithNumericArgument (Ruby 3.1+)
- **Autocorrect:** Yes (Safe)
- **Flags:** `BigDecimal(1.2)` → `BigDecimal('1.2')`
- **Why:** String init is faster than Float init.
- **Reason disabled:** Performance depends on value size and type; not universally beneficial.

### Performance/BlockGivenWithExplicitBlock
- **Autocorrect:** Yes (Safe)
- **Flags:** `def foo(&block); do_x if block_given?; end` → `def foo(&block); do_x if block; end`
- **Why:** Direct block check is faster.
- **Reason disabled:** Produces significantly worse performance in some cases.

### Performance/CaseWhenSplat
- **Autocorrect:** Yes (Unsafe; data-dependent)
- **Flags:** `case x; when *arr; ...; when y; ...; end` (move splat to end)
- **Why:** Avoids allocating splat expansion on every check.
- **Reason disabled:** Not guaranteed improvement; data pattern-dependent.

### Performance/Casecmp
- **Autocorrect:** Yes (Unsafe for non-ASCII)
- **Flags:** `str.downcase == 'abc'` → `str.casecmp('ABC').zero?`
- **Why:** `casecmp` is faster for ASCII-only strings.
- **Reason disabled:** Doesn't work with non-ASCII characters (e.g., Unicode).

### Performance/ChainArrayAllocation
- **Autocorrect:** No
- **Flags:** `array.compact.flatten.map { ... }` → Use mutating methods.
- **Why:** Avoid intermediate array allocations.
- **Reason disabled:** No autocorrect available; requires manual review.

### Performance/CollectionLiteralInLoop
- **Autocorrect:** No
- **Flags:** `users.select { |u| %i[admin, user].include?(u.role) }`
- **Why:** Extract literal arrays/hashes outside loop to avoid re-allocation.
- **Note:** Ruby 3.4+ optimizes certain array literals in method args.

### Performance/ConcurrentMonotonicTime
- **Autocorrect:** Yes (Safe)
- **Flags:** `Concurrent.monotonic_time` → `Process.clock_gettime(Process::CLOCK_MONOTONIC)`
- **Why:** `Process.clock_gettime` is the modern, faster API.

### Performance/ConstantRegexp
- **Autocorrect:** Yes (Safe)
- **Flags:** `pattern.match?(/\A#{SEPARATOR}\Z/)` (in loop/method)
- **Why:** Extract regex to constant to avoid re-compiling.

### Performance/Detect (disabled variant)
- **Autocorrect:** Yes (Unsafe)
- **Flags:** `Hash.select { ... }.first` → `detect` not applicable.
- **Why:** `Hash#select` returns hash, not array; `detect` may not work.

### Performance/InefficientHashSearch
- **Autocorrect:** Yes (Unsafe if receiver not Hash)
- **Flags:** `hash.keys.include?(key)` → `hash.key?(key)`
- **Why:** O(1) lookup vs O(n) array search.
- **Reason disabled:** Can't always detect Hash receiver type.

### Performance/IoReadlines
- **Autocorrect:** Yes (Safe)
- **Flags:** `File.readlines('file').each { |l| puts l }` → `File.open('file').each_line { |l| puts l }`
- **Why:** `each_line` streams; avoids loading entire file into memory.

### Performance/MapCompact (Ruby 2.7+)
- **Autocorrect:** No
- **Flags:** `array.map { ... }.compact` → `array.filter_map { ... }`
- **Why:** `filter_map` is single-pass.
- **Reason disabled:** `filter_map` filters falsey values, not just nil.

### Performance/MapMethodChain
- **Autocorrect:** No
- **Flags:** `array.map(&:foo).map(&:bar)` → `array.map { |x| x.foo.bar }`
- **Why:** Single block is faster; avoids intermediate array.
- **Reason disabled:** No autocorrect; block variable name ambiguous.

### Performance/MethodObjectAsBlock
- **Autocorrect:** No
- **Flags:** `array.map(&method(:foo))` → `array.map { |x| foo(x) }`
- **Why:** Explicit block is faster; avoids method object.

### Performance/OpenStruct
- **Autocorrect:** No
- **Flags:** `OpenStruct.new(...)` → `Struct.new(...)`
- **Why:** `OpenStruct` invalidates Ruby global method cache on instantiation.
- **Reason disabled:** `OpenStruct` and `Struct` are not equivalent.

### Performance/RangeInclude
- **Autocorrect:** Yes (Unsafe for non-comparable)
- **Flags:** `(1..100).include?(50)` → `(1..100).cover?(50)`
- **Why:** `cover?` does O(1) comparison vs `include?` O(n) iteration.
- **Reason disabled:** Not equivalent for all types (e.g., `('a'..'z').cover?('yellow')` ≠ `include?`).

### Performance/RedundantEqualityComparisonBlock
- **Autocorrect:** Yes (Unsafe; behavior-altering)
- **Flags:** `items.all? { |x| pattern === x }` → `items.all?(pattern)`
- **Why:** Avoid block overhead; use operator overloading.
- **Reason disabled:** `===` and `==` don't always behave the same.

### Performance/RedundantMerge
- **Autocorrect:** Yes (Unsafe if receiver not Hash)
- **Flags:** `hash.merge!(a: 1)` → `hash[:a] = 1`
- **Why:** Direct assignment is faster than merge.
- **Reason disabled:** Can't always detect Hash receiver.

### Performance/RedundantSortBlock
- **Autocorrect:** Yes (Safe)
- **Flags:** `array.sort { |a, b| a <=> b }` → `array.sort`
- **Why:** Default sort is faster; no block overhead.

### Performance/RedundantSplitRegexpArgument
- **Autocorrect:** Yes (Safe)
- **Flags:** `'a,b,c'.split(/,/)` → `'a,b,c'.split(',')`
- **Why:** String argument is faster than regex for literal splits.

### Performance/RedundantStringChars
- **Autocorrect:** Yes (Partially safe)
- **Flags:** `str.chars[0]` → `str[0]`
- **Why:** Avoid allocating array of characters.

### Performance/SelectMap (Ruby 2.7+)
- **Autocorrect:** No
- **Flags:** `array.select(&:foo).map(&:bar)` → `array.filter_map { |o| o.bar if o.foo }`
- **Why:** Single-pass; avoids intermediate array.
- **Reason disabled:** No autocorrect; requires manual rewrite.

### Performance/SortReverse
- **Autocorrect:** Yes (Safe)
- **Flags:** `array.sort { |a, b| b <=> a }` → `array.sort.reverse`
- **Why:** Reverse after sort is faster than reversing comparison.

### Performance/Squeeze
- **Autocorrect:** Yes (Safe)
- **Flags:** `str.gsub(/a+/, 'a')` → `str.squeeze('a')`
- **Why:** Dedicated method is faster than regex.

### Performance/StringBytesize
- **Autocorrect:** Yes (Unsafe for non-String)
- **Flags:** `string.bytes.count` → `string.bytesize`
- **Why:** `bytesize` returns size directly; `bytes.count` allocates array.

### Performance/Sum
- **Autocorrect:** Yes (Unsafe without initial value)
- **Flags:** `array.reduce(:+)` → `array.sum`
- **Why:** `sum` is optimized; avoids block overhead.
- **Reason disabled:** Risk of type errors if initial value not explicit.

### Performance/UnfreezeString (Ruby 2.3+)
- **Autocorrect:** Yes (Unsafe for encoding differences)
- **Flags:** `'string'.dup` → `+'string'` (unary plus)
- **Why:** Unary plus is faster than `dup`.
- **Reason disabled:** Encoding differences in some cases.

### Performance/ZipWithoutBlock
- **Autocorrect:** Yes (Unsafe for non-Enumerable)
- **Flags:** `[1, 2, 3].map { |id| [id] }` → `[1, 2, 3].zip`
- **Why:** `zip` is faster.
- **Reason disabled:** Only works for Enumerable.

---

## Pending (New or Under Development)

### Performance/AncestorsInclude
- **Autocorrect:** Yes (Unsafe)
- **Flags:** `A.ancestors.include?(B)` → `A <= B`
- **Why:** Operator is faster.
- **Status:** Pending; may have false positives.

### Performance/ArraySemiInfiniteRangeSlice
- **Autocorrect:** Yes (Unsafe for strings)
- **Flags:** `array[2..]` → `array.drop(2)`
- **Why:** Dedicated method is clearer.
- **Status:** Disabled by default (known microbenchmark mistake).

---

## Configuration Skeleton

```yaml
# .rubocop.yml
require:
  - rubocop-performance

Performance:
  Enabled: true
  Severity: refactor

# Enable high-value disabled-by-default cops
Performance/InefficientHashSearch:
  Enabled: true

Performance/OpenStruct:
  Enabled: true

Performance/RangeInclude:
  Enabled: true

Performance/Sum:
  Enabled: true
  SafeAutoCorrect: true

Performance/ConstantRegexp:
  Enabled: true

# Exclude cops or files
Performance/Count:
  Exclude:
    - spec/**/*
    - db/seeds.rb

Performance/Size:
  Exclude:
    - legacy/**/*
```

---

## Rails-Specific Guidance

### Safe Cops for Rails
These are safe to enable and fix in Rails apps without special considerations:

- `Performance/CompareWithBlock` — Use `sort_by`
- `Performance/FlatMap` — Use `flat_map`
- `Performance/ReverseEach` — Use `reverse_each`
- `Performance/StringReplacement` — Use `tr` / `delete`
- `Performance/RegexpMatch` — Use `match?`
- `Performance/DoubleStartEndWith` — Combine method args

### Caution Cops for Rails
These require awareness of Rails versions or patterns:

- `Performance/Count` — Unsafe for ActiveRecord < 5.1; use `to_a.count { ... }` if needed.
- `Performance/Size` — `ActiveRecord::Relation#size` already optimized; usually OK.
- `Performance/Detect` — Safe on arrays, but watch for custom Enumerable implementations.
- `Performance/InefficientHashSearch` — Enable it; Rails uses this pattern frequently.

### Not Recommended for Rails
These have limited applicability or high false-positive rates:

- `Performance/OpenStruct` — Use `Struct` or custom classes instead.
- `Performance/CaseWhenSplat` — Data-dependent; enable if you profile and confirm benefit.
- `Performance/Casecmp` — Unsafe with international strings.

---

## References

- [RuboCop Performance Documentation](https://docs.rubocop.org/rubocop-performance/latest/)
- [Ruby Enum Documentation](https://ruby-doc.org/core/Enumerable.html)
- [Rails Performance Optimization](https://guides.rubyonrails.org/performance_testing.html)
