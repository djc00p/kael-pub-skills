# Common Rails CI Failure Patterns

## Factory / Validation Errors

### `RecordInvalid: Validation failed: Role can't be blank`
New validation added to a join table without updating factories/seeds.
- **Fix**: Add default value to migration column OR explicitly set the field in factories and seeds
- **Check**: `spec/factories/`, `db/seeds.rb`, `db/migrate/`

### `User must be a driver to create a driver profile`
Missing role trait in factory setup.
- **Fix**: Use `create(:user, :driver)` not `create(:user)`

### `BusinessProfile wrong association key`
- **Fix**: Use `owner:` not `user:` when creating BusinessProfile

### `Vehicle missing primary_driver`
- **Fix**: Always set `primary_driver:` when creating vehicles for drivers

## Asset Pipeline

### `The asset "tailwind.css" is not present in the asset pipeline`
Tailwind not compiled in test environment.
- **Fix**: `rails assets:precompile RAILS_ENV=test`

## Migration Errors

### `PendingMigrationError`
- **Fix**: `rails db:migrate RAILS_ENV=test`

## System Specs / Browser

### System specs hanging with no output
- **Cause**: Missing browser driver (geckodriver for Firefox, chromedriver for Chrome)
- **Fix**: Install the appropriate driver and ensure it's in PATH

### WebMock blocking localhost
- **Fix**: Add to `rails_helper.rb`:
  ```ruby
  WebMock.disable_net_connect!(allow_localhost: true)
  ```

## Join Tables Without Primary Key

### `ActiveRecord::MissingRequiredOrderError` on `.last` or `.first`
Join tables with `id: false` can't use `.last`/`.first`.
- **Fix**: Use scoped query instead: `Model.find_by(field: value)`

## Seed Data

### Seeds fail on new validations
When new required columns are added, seed data creation breaks.
- **Fix**: Update `db/seeds.rb` to include the new required fields explicitly

## Debug Approach

For sub-agent debugging (non-interactive):
```ruby
pp object                    # inspect any object
raise object.inspect         # force output and halt
puts object.class            # check type
puts object.errors.full_messages.inspect  # AR errors
```

For local debugging (interactive):
```ruby
binding.pry                  # drop into pry session
```
Never commit `binding.pry` or debug logging — remove before pushing.
