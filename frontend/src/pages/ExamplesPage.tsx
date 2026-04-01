import React, { useState } from 'react';
import { Play, Download, Eye } from 'lucide-react';

interface Example {
  id: string;
  name: string;
  description: string;
  category: string;
  solver: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

const EXAMPLES: Example[] = [
  {
    id: 'cantilever-beam',
    name: 'Cantilever Beam',
    description: 'Fixed beam with point load at tip. Compare FEA with Euler-Bernoulli analytical solution.',
    category: 'Structural',
    solver: 'fea_classic',
    difficulty: 'beginner',
  },
  {
    id: 'simply-supported',
    name: 'Simply Supported Beam',
    description: 'Beam supported at both ends with uniform distributed load.',
    category: 'Structural',
    solver: 'fea_classic',
    difficulty: 'beginner',
  },
  {
    id: 'thermal-plate',
    name: 'Thermal Plate',
    description: '2D heat conduction in a steel plate with fixed temperature boundaries.',
    category: 'Thermal',
    solver: 'thermal_classic',
    difficulty: 'beginner',
  },
  {
    id: 'thermal-transient',
    name: 'Cooling Plate',
    description: 'Transient thermal analysis of a hot plate cooling in ambient air.',
    category: 'Thermal',
    solver: 'thermal_classic',
    difficulty: 'intermediate',
  },
  {
    id: 'l-shaped-bracket',
    name: 'L-Shaped Bracket',
    description: 'Stress concentration in an L-shaped bracket under load.',
    category: 'Structural',
    solver: 'fea_classic',
    difficulty: 'intermediate',
  },
  {
    id: 'cavity-flow',
    name: 'Lid-Driven Cavity',
    description: 'Classic CFD benchmark: 2D flow in a square cavity with moving top wall.',
    category: 'Fluid',
    solver: 'fluid_classic',
    difficulty: 'advanced',
  },
  {
    id: 'modal-analysis',
    name: 'Modal Analysis',
    description: 'Natural frequency extraction for a rectangular plate.',
    category: 'Dynamic',
    solver: 'fea_classic',
    difficulty: 'intermediate',
  },
  {
    id: 'buckling-column',
    name: 'Column Buckling',
    description: 'Euler buckling of a slender column. Compare with critical load formula.',
    category: 'Stability',
    solver: 'fea_classic',
    difficulty: 'advanced',
  },
];

const difficultyColors = {
  beginner: 'bg-emerald-100 text-emerald-700',
  intermediate: 'bg-amber-100 text-amber-700',
  advanced: 'bg-red-100 text-red-700',
};

const ExamplesPage: React.FC = () => {
  const [filter, setFilter] = useState<string>('all');

  const categories = ['all', ...new Set(EXAMPLES.map((e) => e.category))];
  const filtered = filter === 'all' ? EXAMPLES : EXAMPLES.filter((e) => e.category === filter);

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Examples</h1>
        <p className="text-slate-500 mt-1">
          Pre-configured simulations to learn from
        </p>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === cat
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            {cat === 'all' ? 'All' : cat}
          </button>
        ))}
      </div>

      {/* Examples Grid */}
      <div className="grid md:grid-cols-2 gap-4">
        {filtered.map((example) => (
          <div
            key={example.id}
            className="bg-white rounded-2xl border border-slate-200 p-6 hover:border-blue-200 hover:shadow-md transition-all"
          >
            <div className="flex items-start justify-between mb-3">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${difficultyColors[example.difficulty]}`}>
                {example.difficulty}
              </span>
              <span className="text-xs text-slate-400">{example.solver}</span>
            </div>

            <h3 className="text-lg font-semibold text-slate-900 mb-1">
              {example.name}
            </h3>
            <p className="text-sm text-slate-500 mb-4">{example.description}</p>

            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                <Play size={14} />
                Run
              </button>
              <button className="flex items-center gap-1.5 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors">
                <Eye size={14} />
                View
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ExamplesPage;
