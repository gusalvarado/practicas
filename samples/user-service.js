// User Service - Ejemplo con problemas de calidad
const express = require("express");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const mongoose = require("mongoose");

const app = express();
app.use(express.json());

// Problema 1: Hardcoded secrets
const JWT_SECRET = "my-secret-key";
const DB_URL = "mongodb://localhost:27017/users";

// Problema 2: Modelo sin validación
const UserSchema = new mongoose.Schema({
  name: String,
  email: String,
  password: String,
  age: Number,
});

const User = mongoose.model("User", UserSchema);

// Problema 3: Función muy larga y compleja
app.post("/register", async (req, res) => {
  try {
    const { name, email, password, age } = req.body;

    // Problema 4: Validación insuficiente
    if (!email || !password) {
      return res.status(400).json({ error: "Email and password required" });
    }

    // Problema 5: Lógica de negocio en el controlador
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ error: "User already exists" });
    }

    // Problema 6: Sin validación de fortaleza de contraseña
    const hashedPassword = await bcrypt.hash(password, 10);

    const user = new User({
      name,
      email,
      password: hashedPassword,
      age,
    });

    await user.save();

    // Problema 7: Token sin expiración
    const token = jwt.sign({ userId: user._id }, JWT_SECRET);

    res.status(201).json({
      message: "User created successfully",
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        age: user.age,
      },
    });
  } catch (error) {
    // Problema 8: Manejo de errores genérico
    console.error("Registration error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Problema 9: Función duplicada (lógica similar en login)
app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: "Email and password required" });
    }

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ error: "Invalid credentials" });
    }

    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(400).json({ error: "Invalid credentials" });
    }

    const token = jwt.sign({ userId: user._id }, JWT_SECRET);

    res.json({
      message: "Login successful",
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        age: user.age,
      },
    });
  } catch (error) {
    console.error("Login error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Problema 10: Sin middleware de autenticación
app.get("/profile", async (req, res) => {
  try {
    const token = req.headers.authorization?.split(" ")[1];

    if (!token) {
      return res.status(401).json({ error: "No token provided" });
    }

    // Problema 11: Sin manejo de errores de JWT
    const decoded = jwt.verify(token, JWT_SECRET);
    const user = await User.findById(decoded.userId);

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    res.json({
      id: user._id,
      name: user.name,
      email: user.email,
      age: user.age,
    });
  } catch (error) {
    console.error("Profile error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Problema 12: Sin validación de entrada
app.put("/profile", async (req, res) => {
  try {
    const token = req.headers.authorization?.split(" ")[1];
    const { name, age } = req.body;

    if (!token) {
      return res.status(401).json({ error: "No token provided" });
    }

    const decoded = jwt.verify(token, JWT_SECRET);
    const user = await User.findById(decoded.userId);

    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    // Problema 13: Actualización sin validación
    user.name = name || user.name;
    user.age = age || user.age;

    await user.save();

    res.json({
      message: "Profile updated successfully",
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        age: user.age,
      },
    });
  } catch (error) {
    console.error("Update profile error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Problema 14: Sin rate limiting
// Problema 15: Sin logging estructurado
// Problema 16: Sin documentación de API
// Problema 17: Sin tests
// Problema 18: Sin configuración de CORS
// Problema 19: Sin manejo de conexión a DB
// Problema 20: Sin graceful shutdown

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`User service running on port ${PORT}`);
});

module.exports = app;
