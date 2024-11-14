class EvaluadorCredito:
    def __init__(self):
        # Pesos para diferentes factores de scoring
        self.pesos = {
            'historial_pagos': 0.30,
            'ingresos': 0.25,
            'estabilidad_laboral': 0.20,
            'referencias': 0.15,
            'ubicacion': 0.10
        }
        
        # Límites de crédito según score
        self.limites_credito = {
            'alto': 2000000,    # 2 millones COP
            'medio': 1000000,   # 1 millón COP
            'bajo': 500000      # 500 mil COP
        }
        
        # Tasas de interés según score (mensual)
        self.tasas_interes = {
            'alto': 0.05,    # 5% mensual
            'medio': 0.08,   # 8% mensual
            'bajo': 0.10     # 10% mensual
        }

    def calcular_score(self, datos_cliente):
        """
        Calcula el score crediticio basado en la información básica del cliente
        """
        score = 0
        
        # Evaluación de historial de pagos (0-100)
        if datos_cliente['historial_pagos'] >= 80:
            score += 100 * self.pesos['historial_pagos']
        elif datos_cliente['historial_pagos'] >= 60:
            score += 70 * self.pesos['historial_pagos']
        else:
            score += 40 * self.pesos['historial_pagos']
        
        # Evaluación de ingresos mensuales
        ingreso_minimo = 1000000  # 1 millón COP
        score_ingresos = min(100, (datos_cliente['ingresos'] / ingreso_minimo) * 100)
        score += score_ingresos * self.pesos['ingresos']
        
        # Evaluación de estabilidad laboral (meses)
        if datos_cliente['meses_trabajo'] >= 12:
            score += 100 * self.pesos['estabilidad_laboral']
        elif datos_cliente['meses_trabajo'] >= 6:
            score += 70 * self.pesos['estabilidad_laboral']
        else:
            score += 40 * self.pesos['estabilidad_laboral']
        
        # Evaluación de referencias
        score += datos_cliente['score_referencias'] * self.pesos['referencias']
        
        # Evaluación de ubicación (según zona de riesgo)
        score += datos_cliente['score_ubicacion'] * self.pesos['ubicacion']
        
        return score

    def determinar_nivel_riesgo(self, score):
        """
        Determina el nivel de riesgo basado en el score
        """
        if score >= 75:
            return 'alto'
        elif score >= 60:
            return 'medio'
        else:
            return 'bajo'

    def calcular_prestamo(self, datos_cliente):
        """
        Calcula el monto máximo, tasa de interés y cuota mensual
        """
        score = self.calcular_score(datos_cliente)
        nivel_riesgo = self.determinar_nivel_riesgo(score)
        
        monto_maximo = self.limites_credito[nivel_riesgo]
        tasa_interes = self.tasas_interes[nivel_riesgo]
        
        # Calcula cuota mensual (préstamo a 3 meses)
        plazo_meses = 3
        cuota_mensual = (monto_maximo * (1 + tasa_interes)) / plazo_meses
        
        return {
            'score': round(score, 2),
            'nivel_riesgo': nivel_riesgo,
            'monto_maximo': monto_maximo,
            'tasa_interes_mensual': tasa_interes * 100,
            'plazo_meses': plazo_meses,
            'cuota_mensual': round(cuota_mensual, 2)
        }

# Ejemplo de uso
def main():
    evaluador = EvaluadorCredito()
    
    # Datos de ejemplo de un cliente
    datos_cliente = {
        'historial_pagos': 70,          # Score de 0-100
        'ingresos': 1200000,            # Ingresos mensuales en COP
        'meses_trabajo': 8,             # Meses en trabajo actual
        'score_referencias': 80,         # Score de referencias (0-100)
        'score_ubicacion': 70           # Score de ubicación (0-100)
    }
    
    resultado = evaluador.calcular_prestamo(datos_cliente)
    
    print("\n=== Resultado de Evaluación de Crédito ===")
    print(f"Score crediticio: {resultado['score']}")
    print(f"Nivel de riesgo: {resultado['nivel_riesgo']}")
    print(f"Monto máximo aprobado: ${resultado['monto_maximo']:,} COP")
    print(f"Tasa de interés mensual: {resultado['tasa_interes_mensual']}%")
    print(f"Plazo del préstamo: {resultado['plazo_meses']} meses")
    print(f"Cuota mensual estimada: ${resultado['cuota_mensual']:,} COP")

if __name__ == "__main__":
    main()