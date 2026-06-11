# MCP Templates Quick Reference

## Available Resources

All templates are exposed as MCP resources and can be accessed through the AI Banking MCP server.

### Resource URIs

```
template://home         → Home Screen UI (account balance, transactions)
template://transaction  → Transaction Screen UI (analytics, budget)
template://menu         → Menu Screen UI (profile, navigation)
template://list         → List all available templates
```

## Usage Examples

### In Claude/Cursor
```
@template-home          # Get home screen template
@template-transaction   # Get transaction screen template
@template-menu          # Get menu screen template
```

### Programmatically

```python
from mcp.templates_resource import get_home_template, get_transaction_template, get_menu_template

html_home = get_home_template()
html_transaction = get_transaction_template()
html_menu = get_menu_template()
```

## Features

✅ **3 Complete UI Screens**
- Home: Dashboard with balance and transactions
- Transaction: Analytics with budget breakdown
- Menu: Profile and navigation menu

✅ **MCP Integration**
- Exposed as @mcp.resource decorators
- Accessible via template:// URIs
- Automatically registered on server startup

✅ **Production Ready**
- Modern responsive design
- Gradient UI with smooth animations
- Mobile optimized (375px width)
- No external dependencies

## File Locations

```
ai_banking/
├── templates_resource.py    ← MCP resource definitions
├── templates/               ← HTML template folder
│   ├── home.html
│   ├── transaction.html
│   ├── menu.html
│   └── README.md           ← Template documentation
└── main.py                 ← Imports templates_resource
```

## Next Steps

1. **View Templates**: Open any `.html` file in browser to preview
2. **Customize**: Edit colors, text, or layout in the HTML files
3. **Deploy**: Serve templates via web server or static file hosting
4. **Integrate**: Use in your application or embed in web pages

---

**Created**: March 2026
**Status**: Active & Ready to Use
