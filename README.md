# 🧮 Modern Calculator

A sleek, modern calculator built with Python and Tkinter featuring a dark theme and intuitive interface.


## ✨ Features

- 🎨 **Modern Dark Theme** - Easy on the eyes with a professional appearance
- 🔢 **Basic Operations** - Addition, subtraction, multiplication, and division
- 🔬 **Advanced Functions** - Power operations, square, modulo, and parentheses
- 🥧 **Mathematical Constants** - Pi (π) button for quick access
- ⌨️ **User-Friendly** - Clear display with color-coded buttons
- 🎯 **Error Handling** - Safe expression evaluation with error messages
- 🔙 **Undo Function** - Backspace to correct mistakes

## 📸 Screenshot

```
┌─────────────────────────────────┐
│         Calculator              │
├─────────────────────────────────┤
│                                 │
│         Display Area            │
│                                 │
├─────────────────────────────────┤
│  AC  │  (  │  )  │  ←          │
│   7  │  8  │  9  │  ÷          │
│   4  │  5  │  6  │  ×          │
│   1  │  2  │  3  │  −          │
│   0  │  .  │  π  │  +          │
│  x²  │  ^  │  %  │  =          │
└─────────────────────────────────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/prosper-codes/python_simple_intermediate.git

   ```

2. **Verify Tkinter installation** (optional)
   ```bash
   python -m tkinter
   ```
   If a small window appears, Tkinter is installed correctly.

3. **Run the calculator**
   ```bash
   python calculator.py
   ```

## 💻 Usage

### Basic Operations
- Click number buttons (0-9) to input numbers
- Use operation buttons (+, −, ×, ÷) for calculations
- Press `=` to evaluate the expression
- Use `AC` to clear all
- Use `←` to delete the last character

### Advanced Features
- **Parentheses**: Use `(` and `)` for complex expressions
- **Power**: Use `^` for exponentiation (e.g., 2^3 = 8)
- **Square**: Use `x²` to square a number
- **Modulo**: Use `%` for remainder operations
- **Pi**: Use `π` to insert 3.14159

### Example Calculations
```
Simple: 5 + 3 = 8
Advanced: (2 + 3) × 4 = 20
Power: 2^3 = 8
Square: 5 x² = 25
Pi: π × 2 = 6.28318
```

## 🎨 Color Scheme

| Element | Color | Purpose |
|---------|-------|---------|
| Background | `#1e1e1e` | Main window background |
| Display | `#2d2d2d` | Calculator display |
| Number Buttons | `#3a3a3a` | Number inputs (0-9, .) |
| Operation Buttons | `#505050` | Math operations |
| Special Buttons | `#d32f2f` | AC and backspace |
| Equals Button | `#4CAF50` | Calculate result |
| Accent Color | `#4CAF50` | Operation symbols |

## 🛠️ Technical Details

### Built With
- **Python** - Core programming language
- **Tkinter** - GUI framework
- **AST Module** - Safe expression evaluation

### Key Features
- Object-oriented design with Calculator class
- Safe expression evaluation using Python's AST parser
- No use of dangerous `eval()` with raw strings
- Responsive button layout with grid system
- Custom fonts and styling

## 📝 Code Structure

```
calculator.py
│
├── Calculator Class
│   ├── __init__()          # Initialize window and components
│   ├── create_display()    # Build display area
│   ├── create_buttons()    # Build button grid
│   ├── get_button_command()# Map buttons to functions
│   ├── insert_text()       # Insert characters
│   ├── clear_all()         # Clear display
│   ├── undo()              # Remove last character
│   └── calculate()         # Evaluate expression
│
└── Main execution block
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add scientific calculator functions (sin, cos, tan, log, etc.)
- Implement keyboard support
- Add calculation history
- Create light theme option
- Add unit tests

## 🐛 Known Issues

- Very long expressions may overflow the display
- Complex nested expressions might require parentheses for clarity

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@prosper-codes][(https://github.com/yourusername)](https://github.com/prosper-codes)
- Email:tpjn02@gmail.com

## 🙏 Acknowledgments

- Inspired by modern calculator designs
- Built with Python's Tkinter framework
- Color scheme inspired by material design principles

## 📊 Project Stats

- **Lines of Code**: ~150
- **File Size**: < 10KB
- **Dependencies**: 0 (only standard library)
- **Python Version**: 3.6+

---

⭐ **Star this repository if you find it helpful!**

📢 **Found a bug?** Open an issue!

💡 **Have a feature request?** We'd love to hear it!
