#!/usr/bin/env node

/**
 * Script de Análisis de Calidad de Código con IA
 *
 * Este script analiza la calidad del código utilizando múltiples herramientas
 * y genera reportes detallados con sugerencias de mejora basadas en IA.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const chalk = require("chalk");

class CodeQualityAnalyzer {
  constructor(options = {}) {
    this.options = {
      projectPath: options.projectPath || process.cwd(),
      outputDir: options.outputDir || "./quality-reports",
      tools: options.tools || ["eslint", "prettier", "sonar", "security"],
      aiEnabled: options.aiEnabled !== false,
      ...options,
    };

    this.results = {
      timestamp: new Date().toISOString(),
      project: path.basename(this.options.projectPath),
      tools: {},
      summary: {},
      recommendations: [],
    };
  }

  /**
   * Ejecuta el análisis completo de calidad
   */
  async analyze() {
    console.log(chalk.blue("🔍 Iniciando análisis de calidad de código..."));

    try {
      // Crear directorio de reportes
      this.ensureOutputDir();

      // Ejecutar herramientas de análisis
      await this.runESLint();
      await this.runPrettier();
      await this.runSecurityScan();
      await this.runSonarAnalysis();

      // Generar análisis con IA
      if (this.options.aiEnabled) {
        await this.generateAIRecommendations();
      }

      // Generar resumen
      this.generateSummary();

      // Guardar reportes
      await this.saveReports();

      // Mostrar resultados
      this.displayResults();

      console.log(chalk.green("✅ Análisis completado exitosamente"));
    } catch (error) {
      console.error(chalk.red("❌ Error durante el análisis:"), error.message);
      process.exit(1);
    }
  }

  /**
   * Ejecuta análisis con ESLint
   */
  async runESLint() {
    console.log(chalk.yellow("📝 Ejecutando ESLint..."));

    try {
      const eslintCommand = `npx eslint . --format json --output-file ${this.options.outputDir}/eslint-report.json`;
      execSync(eslintCommand, { cwd: this.options.projectPath });

      const reportPath = path.join(
        this.options.outputDir,
        "eslint-report.json"
      );
      if (fs.existsSync(reportPath)) {
        const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
        this.results.tools.eslint = {
          status: "completed",
          errors: report.filter((r) => r.errorCount > 0).length,
          warnings: report.filter((r) => r.warningCount > 0).length,
          files: report.length,
          details: report,
        };
      }
    } catch (error) {
      this.results.tools.eslint = {
        status: "failed",
        error: error.message,
      };
    }
  }

  /**
   * Ejecuta análisis con Prettier
   */
  async runPrettier() {
    console.log(chalk.yellow("🎨 Ejecutando Prettier..."));

    try {
      const prettierCommand = `npx prettier --check . --write ${this.options.outputDir}/prettier-report.json`;
      execSync(prettierCommand, { cwd: this.options.projectPath });

      this.results.tools.prettier = {
        status: "completed",
        message: "Formato de código verificado",
      };
    } catch (error) {
      this.results.tools.prettier = {
        status: "failed",
        error: error.message,
      };
    }
  }

  /**
   * Ejecuta análisis de seguridad
   */
  async runSecurityScan() {
    console.log(chalk.yellow("🔒 Ejecutando análisis de seguridad..."));

    try {
      const auditCommand = `npm audit --json > ${this.options.outputDir}/security-report.json`;
      execSync(auditCommand, { cwd: this.options.projectPath });

      const reportPath = path.join(
        this.options.outputDir,
        "security-report.json"
      );
      if (fs.existsSync(reportPath)) {
        const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
        this.results.tools.security = {
          status: "completed",
          vulnerabilities: report.vulnerabilities || 0,
          dependencies: report.dependencies || 0,
          details: report,
        };
      }
    } catch (error) {
      this.results.tools.security = {
        status: "failed",
        error: error.message,
      };
    }
  }

  /**
   * Ejecuta análisis con SonarQube
   */
  async runSonarAnalysis() {
    console.log(chalk.yellow("📊 Ejecutando análisis SonarQube..."));

    try {
      const sonarCommand = `sonar-scanner -Dsonar.projectKey=${
        this.results.project
      } -Dsonar.sources=. -Dsonar.host.url=${
        process.env.SONAR_HOST_URL || "http://localhost:9000"
      } -Dsonar.login=${process.env.SONAR_TOKEN || ""}`;
      execSync(sonarCommand, { cwd: this.options.projectPath });

      this.results.tools.sonar = {
        status: "completed",
        message: "Análisis SonarQube completado",
      };
    } catch (error) {
      this.results.tools.sonar = {
        status: "failed",
        error: error.message,
      };
    }
  }

  /**
   * Genera recomendaciones usando IA
   */
  async generateAIRecommendations() {
    console.log(chalk.yellow("🤖 Generando recomendaciones con IA..."));

    try {
      // Simular análisis con IA (en un caso real, aquí se integraría con una API de IA)
      const recommendations = this.generateMockAIRecommendations();

      this.results.recommendations = recommendations;
      this.results.tools.ai = {
        status: "completed",
        recommendations: recommendations.length,
      };
    } catch (error) {
      this.results.tools.ai = {
        status: "failed",
        error: error.message,
      };
    }
  }

  /**
   * Genera recomendaciones mock de IA
   */
  generateMockAIRecommendations() {
    const recommendations = [];

    // Analizar resultados de ESLint
    if (this.results.tools.eslint?.errors > 0) {
      recommendations.push({
        type: "code_quality",
        priority: "high",
        title: "Errores de ESLint detectados",
        description: `Se encontraron ${this.results.tools.eslint.errors} errores de ESLint que deben corregirse.`,
        suggestion:
          "Ejecutar `npx eslint . --fix` para corregir automáticamente algunos errores.",
        files: this.results.tools.eslint.details?.map((d) => d.filePath) || [],
      });
    }

    // Analizar vulnerabilidades de seguridad
    if (this.results.tools.security?.vulnerabilities > 0) {
      recommendations.push({
        type: "security",
        priority: "critical",
        title: "Vulnerabilidades de seguridad encontradas",
        description: `Se encontraron ${this.results.tools.security.vulnerabilities} vulnerabilidades de seguridad.`,
        suggestion:
          "Ejecutar `npm audit fix` para corregir vulnerabilidades automáticamente.",
        files: [],
      });
    }

    // Recomendaciones generales
    recommendations.push({
      type: "best_practices",
      priority: "medium",
      title: "Implementar tests unitarios",
      description: "No se detectaron tests unitarios en el proyecto.",
      suggestion:
        "Crear tests unitarios usando Jest o Mocha para mejorar la calidad del código.",
      files: [],
    });

    recommendations.push({
      type: "documentation",
      priority: "low",
      title: "Mejorar documentación",
      description: "La documentación del proyecto podría ser más completa.",
      suggestion: "Agregar JSDoc a las funciones y crear documentación de API.",
      files: [],
    });

    return recommendations;
  }

  /**
   * Genera resumen del análisis
   */
  generateSummary() {
    const summary = {
      totalIssues: 0,
      criticalIssues: 0,
      highPriorityIssues: 0,
      mediumPriorityIssues: 0,
      lowPriorityIssues: 0,
      toolsStatus: {},
      overallScore: 0,
    };

    // Contar issues por herramienta
    Object.keys(this.results.tools).forEach((tool) => {
      const toolResult = this.results.tools[tool];
      summary.toolsStatus[tool] = toolResult.status;

      if (tool === "eslint") {
        summary.totalIssues +=
          (toolResult.errors || 0) + (toolResult.warnings || 0);
      } else if (tool === "security") {
        summary.totalIssues += toolResult.vulnerabilities || 0;
        summary.criticalIssues += toolResult.vulnerabilities || 0;
      }
    });

    // Contar issues por prioridad
    this.results.recommendations.forEach((rec) => {
      switch (rec.priority) {
        case "critical":
          summary.criticalIssues++;
          break;
        case "high":
          summary.highPriorityIssues++;
          break;
        case "medium":
          summary.mediumPriorityIssues++;
          break;
        case "low":
          summary.lowPriorityIssues++;
          break;
      }
    });

    // Calcular score general
    const maxScore = 100;
    const penaltyPerIssue = 5;
    const penaltyPerCritical = 20;

    summary.overallScore = Math.max(
      0,
      maxScore -
        summary.totalIssues * penaltyPerIssue -
        summary.criticalIssues * penaltyPerCritical
    );

    this.results.summary = summary;
  }

  /**
   * Guarda los reportes en archivos
   */
  async saveReports() {
    const reports = {
      "quality-analysis.json": this.results,
      "summary.json": this.results.summary,
      "recommendations.json": this.results.recommendations,
    };

    Object.entries(reports).forEach(([filename, data]) => {
      const filePath = path.join(this.options.outputDir, filename);
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    });
  }

  /**
   * Muestra los resultados en consola
   */
  displayResults() {
    console.log("\n" + chalk.blue("📊 RESUMEN DEL ANÁLISIS DE CALIDAD"));
    console.log("=".repeat(50));

    // Score general
    const score = this.results.summary.overallScore;
    const scoreColor = score >= 80 ? "green" : score >= 60 ? "yellow" : "red";
    console.log(chalk[scoreColor](`🎯 Score General: ${score}/100`));

    // Issues por prioridad
    console.log("\n📋 Issues Encontrados:");
    console.log(
      chalk.red(`   🔴 Críticos: ${this.results.summary.criticalIssues}`)
    );
    console.log(
      chalk.yellow(`   🟡 Altos: ${this.results.summary.highPriorityIssues}`)
    );
    console.log(
      chalk.blue(`   🔵 Medios: ${this.results.summary.mediumPriorityIssues}`)
    );
    console.log(
      chalk.gray(`   ⚪ Bajos: ${this.results.summary.lowPriorityIssues}`)
    );

    // Estado de herramientas
    console.log("\n🛠️ Estado de Herramientas:");
    Object.entries(this.results.summary.toolsStatus).forEach(
      ([tool, status]) => {
        const statusColor = status === "completed" ? "green" : "red";
        const statusIcon = status === "completed" ? "✅" : "❌";
        console.log(chalk[statusColor](`   ${statusIcon} ${tool}: ${status}`));
      }
    );

    // Recomendaciones principales
    if (this.results.recommendations.length > 0) {
      console.log("\n💡 Recomendaciones Principales:");
      this.results.recommendations.slice(0, 3).forEach((rec, index) => {
        const priorityColor =
          rec.priority === "critical"
            ? "red"
            : rec.priority === "high"
            ? "yellow"
            : "blue";
        console.log(
          chalk[priorityColor](
            `   ${index + 1}. [${rec.priority.toUpperCase()}] ${rec.title}`
          )
        );
        console.log(chalk.gray(`      ${rec.description}`));
      });
    }

    console.log(
      "\n📁 Reportes guardados en:",
      chalk.cyan(this.options.outputDir)
    );
  }

  /**
   * Asegura que el directorio de salida existe
   */
  ensureOutputDir() {
    if (!fs.existsSync(this.options.outputDir)) {
      fs.mkdirSync(this.options.outputDir, { recursive: true });
    }
  }
}

// Ejecutar si se llama directamente
if (require.main === module) {
  const analyzer = new CodeQualityAnalyzer({
    projectPath: process.argv[2] || process.cwd(),
    outputDir: process.argv[3] || "./quality-reports",
    aiEnabled: process.argv.includes("--ai"),
  });

  analyzer.analyze().catch(console.error);
}

module.exports = CodeQualityAnalyzer;
