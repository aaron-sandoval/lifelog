��    *      l              �     �  �   �  d   �  �   �     �     �     �     �     �  =     G   B     �  C   �  5   �  h  $     �  	   �     �  �   �     �  
   �     �  �  �  �   �
  �   M  �   �     ~  ]   �     �  �  �  ,  �  �  �     �     �  0   �  ;        G    O     �     �     �  �  �     �  �   �  |   |  �   �     �     �     �     �       F   &  R   m  %   �  F   �  >   -  �  l     �     �     
  �                  /  �   =  �   
  �   �  �   �     z   O   �      �     �   A  �"  �  ?$     �%     �%  -   
&  9   8&     r&  �  ~&     S)     `)     h)   **Future work** - Check out the spikes about 24 hours noted above.
- Add labels for smaller events like the short cycle tours in 2019 and 2021.
- Split this plot into 2 subplots looking at weekdays and weekends. - Media consumed
- People I spend time with
- Food
- Location
- Subject matters researched/discussed - {0}: Working, career planning
- {1}: Studying, independent learning and projects
- {2}: Transport, researching, email, chores, the 'everything else' bucket
- {3}: Fun stuff
- {4}: :sleeping: 2017
Cornell 2022
Cycle Tour 2022
Tour End 2022
Tour Start 2023
Career Pivot Average Person-Hours of Social Interaction per Day, by Gender Average Person-Hours of Social Interaction per Day, by Primary Relation Deep Lifelog Data Analysis DEMO Distributions of Time of Falling Asleep and Waking Up by Life Phase Duration by Metaproject per Day, Averaged over 1 Week Errors in `Metaproject` attribution mostly come from `Project` instances which don't cleanly fit into a single `Metaproject`. For example, `Project.{5}` contains tasks for both rec riding and bike maintenance, which belong to {3} and {2}, respectively. Some of these split attribution cases have been handled in data cleaning, but I haven't caught all of them. Fall asleep First
Job Grad
School I like how this plot illustrates the phases of my adult life with different `Metaproject` focus. You can easily see the shifts from grad school, to working, to long-haul cycle touring in 2022, and to independent study in 2023.  Introduction Life Phase Metaprojects Much of the design work in this project has been in abstracting as much as possible about daily activities into data structures like `Project`, `Tag`, `Collectible`, etc. At the top of the `Project` taxonomy is the `Metaproject`, a set of 5 broad categories which together contain every `Project`. This is a useful data feature to begin with in a top-down analysis approach, since major shifts in lifestyle are evident while smaller details don't muddy the waters. Or comparing how overworked I was in grad school vs in the busiest periods in my first job. Grad school was consistently more consuming than work, with only 2 spikes around 2021-01 coming close.  Or how as my studies in Spring 2018 gradually ate up more time over the course of the semester, it was mostly {0} which was sacrificed, {1} only dropping a bit.  Or the big zero-sum spike-trough pairs poking above the 24-hour total line. I'm not sure what is causing them. Most likely some unclean data.  Person index Spanish translations across the site are in work. Apologies for any confusion this may cause. Start
First Job The {0} prevalence is obvious. The right subplot shows the overall proportion of time by gender, with {0} occupying around 75% of the total. Grad school in the first half of 2018 was clearly {0}-dominated. That eased up in 2019, when, I hypothesize, my job became more collaborative within a gender-balanced team. Spikes around July, November, or December make sense, since that's when I usually visit my dad's family and spend time with my grandma, aunts, and cousins. There's so much to see in the details of this plot. Like how data collection was consistently incomplete until 2018-06. This is probably because, when I started my first job, I used this same data to fill in my timesheet at work, and I got into the habit of logging data more precisely at all hours.  Though all of those features are in the data, there is more feature engineering and visualization work to be done. In addition to being an exercise in data analysis and software engineering, this project is also a mode of introspection, one more objective than fallible memory. Of course, this is all going to be much more interesting to me that it is to anyone else, so I'll try to focus on relatable ideas before diving down weird rabbit holes. Time of day Total
Person-Hours Total Time Spent
 with Individual People, Sorted Total Time Spent
 with Individual People, Sorted, Log Scale Wake up Welcome to Deep Lifelog, my first serious data analysis project! Since I started grad school in September 2017, I've collected continuous time series tabular data on my daily activities. It started as a small productivity exercise to track my academic tasks, but as my data obsession kicked in the scope ballooned out of control :smile:. I was inspired by [r/dataisbeautiful content like this](https://www.reddit.com/r/dataisbeautiful/comments/ab4uzz/i_recorded_every_hour_of_my_2018_and_17_oc/), but I wanted to track way more detail than a single categorical variable over fixed intervals. Over the years, I've adding data features like: [hours/day] [hours] [person-hours/day] Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2024-04-30 23:09-0600
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: es_MX
Language-Team: es_MX <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.11.0
 **Para completar** - Investigar los picos sobre 24 horas mencionados arriba.
- Agregar etiquetas a eventos de menor importancia como las giras de bici cortas en 2019 y 2021.
- Divida esta gráfico en 2 para los días y los fines de semana. - Los medios consumidos
- Las personas con quienes interactúo
- La comida
- La ubicación
- Las temas que investigo/discuto - {0}: Trabajar, planear la carrera
- {1}: Estudiar, proyectos y aprendizaje independiente
- {2}: Transporte, investigar, email, tareas domésticas, la categoría 'el resto'
- {3}: Divertirse
- {4}: :sleeping: 2017
Cornell 2022
Gira en Bici 2022
Fin de Gira 2022
Inicio de Gira 2023
Cambio de Carrera Promedio de Persona-Horas de Interacción Social por Día, por Género Promedio de Persona-Horas de Interacción Social por Día, por Relación Principal Deep Lifelog Análisis de Datos MANÍ Distribuciones de la Hora de Dormirse y Levantarse por Fase de la Vida Duración por Metaproyecto por Día, Promedio durante 1 Semana Errores en atribución de `Metaproyecto` suelen originar desde instancias de `Proyecto` los cuales no encajan en un solo `Metaproyecto`. Por ejemplo, `Proyecto.{5}` contiene tareas de montar en bici y mantener la bici, las cuales encajan en {3} y {2}, respectivamente. Algunos de estes casos de atribución dividida ya han sido resueltos por la limpia de datos, pero no he notado al 100%.  Dormirse Primer
Trabajo Posgrado Me gusta cómo este gráfico ilustra las fases de mi vida adulta con diferentes enfoques de `Metaproyecto`. Puedes ver fácilmente los cambios desde el posgrado, el trabajo, el cicloturismo de larga distancia en 2022 y el estudio independiente en 2023.  Introducción Fase de la Vida Metaproyectos Gran parte del trabajo de diseño en este proyecto ha consistido en abstraer tanto como sea posible sobre las actividades diarias en estructuras de datos como `Proyecto`, `Etiqueta`, `Coleccionable`, etc. O comparar el exceso de trabajo que tenía en el posgrado con los períodos más ocupados de mi primer trabajo. El posgrado consumía consistentemente más que el trabajo, con solo 2 picos alrededor de 2021-01 acercándose.  O cómo a medida que mis estudios en la primavera de 2018 consumieron gradualmente más tiempo a lo largo del semestre, fue principalmente {0} lo que se sacrificó, y {1} solo disminuyó un poco.  O los grandes pares de picos y valles de suma cero que se asoman por encima de la línea total de 24 horas. No estoy seguro de qué los está causando. Lo más probable es que se trate de datos sucios. Índice de persona Las traducciones al español están en progreso. Discúlpame por la confusión. Empezar
Primer Trabajo El predominio de {0} es obvio.  El gráfico a la derecha muestra la proporción de tiempo total por género, y {0} ocupa un 75% del total. El posgrado en la primera mitad de 2018 era claramente dominado por {0}. Este patrón se disminuyó en 2019 cuando, yo hipotetizo, mi trabajo se volvió más colaborativo dentro de un equipo de balancia entre géneros. Picos en julio, noviembre, o diciembre tienen razón, puesto que estes meses suelo visitar a la familia de mi papá y pasar tiempo con mi abuela, tías, y primos. Hay tan mucho que ver el los detalles del gráfico. Cómo la recolección de datos no era completo consistentemente hasta 2018-06. Probablemente se debe a que cuando empecé mi primer trabajo, usaba estes mismos datos para llenar mi hoja de horas, y me acostumbré a registrar los datos más precisamente todo el tiempo.  Aunque todas estas características están presentes en los datos, todavía queda mucho más ingeniería de características y trabajo de visualización. Además que datos y informática, este proyecto también es un modo de introspeccionar más objetivo que la memoria falible. Por supuesto, todo me interesa a mí más que al resto de mundo, así que intento enfocar en los ideas relacionables antes de meterme en cosas turbias. Hora Persona-Horas
en Total Tiempo Total Pasado
 con Individuos, Ordenado Tiempo Total Pasado
 con Individuos, Ordenado, Escala Log Despertarse ¡Bienvenidos a Deep Lifelog (Registro Profundo de la Vida), mi primer proyecto serio de análisis de datos! Desde que empecé el posgrado en 2017, yo collecionaba datos tabulares de series de tiempo continuos sobre mis actividades cotidianas. Al principio se intentaba para seguir mis tareas académicas, pero mientras que mi obsesión por los datos se surgió, el alcance del proyecto se infló fuera de control :smile:. Me inspiró [contenido de r/dataisbeautiful como esto](https://www.reddit.com/r/dataisbeautiful/comments/ab4uzz/i_recorded_every_hour_of_my_2018_and_17_oc/), pero quería rastrear mucho más que una sola variable categórica en intervalos fijados. A través del tiempo, añadía características como: [horas/día] [horas] [persona-horas/día] 