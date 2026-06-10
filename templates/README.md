# Banking App UI Templates

This folder contains HTML templates for the AI Banking application UI, based on the modern banking app design. All templates are exposed as MCP (Model Context Protocol) resources.

## Templates

### 1. **Home** (`template://home`)
The main dashboard showing:
- Account balance card with card details
- Quick action buttons (Transfer, Pay, Accounts)
- Latest transactions list with transaction history
- Bottom navigation bar

### 2. **Transaction** (`template://transaction`)
The transaction analysis screen featuring:
- Card transaction summary
- Monthly vs Yearly selector tabs
- Transaction trend chart
- Monthly budget breakdown
  - Spent vs Remaining statistics
  - Visual progress indicators

### 3. **Menu** (`template://menu`)
The user profile and navigation menu with:
- User profile section (avatar, name, status)
- Organized menu sections:
  - Account (Home, Transaction, Wallet, Card)
  - Settings (Settings, Security, Support, Terms & Privacy)
  - Profile (Edit Profile, Preferences, Logout)

## Design Features

All templates include:
- **Responsive Design**: Optimized for mobile display (375px width)
- **Modern UI**: Gradient backgrounds, smooth transitions, and rounded corners
- **Dark Theme**: Blue gradient background (#1e3a8a to #2563eb)
- **Interactive Elements**: Hover effects and smooth animations
- **Status Bar**: Realistic phone status bar
- **Bottom Navigation**: Consistent navigation across all screens

## Using the Templates

### Access via MCP Resources

```python
# Get home template
@mcp.resource("template://home")

# Get transaction template
@mcp.resource("template://transaction")

# Get menu template
@mcp.resource("template://menu")

# List all available templates
@mcp.resource("template://list")
```

### File Structure

```
templates/
├── home.html          # Home screen template
├── transaction.html   # Transaction screen template
└── menu.html          # Menu screen template
```

## Integration

The templates are registered in `templates_resource.py` and imported in `main.py`:

```python
import templates_resource
```

This automatically exposes all templates as MCP resources when the server starts.

## Customization

Each template can be customized by:
1. Modifying HTML structure in the respective `.html` files
2. Updating CSS styles in the `<style>` section
3. Changing emoji icons and text content
4. Adjusting colors and gradients

## Browser Compatibility

All templates use modern CSS features supported by:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Notes

- Templates use emoji icons for UI elements (can be replaced with icon libraries)
- Responsive design uses CSS Grid and Flexbox
- No external dependencies required - pure HTML/CSS
- Ready to be served as static files or embedded in web applications
