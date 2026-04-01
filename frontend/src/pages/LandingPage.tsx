import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Zap, Gauge, Thermometer, Waves, Cpu, Globe, Github } from 'lucide-react';

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero */}
      <section className="relative py-32 px-6 bg-slate-950 text-white overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px]" />

        <div className="relative max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium mb-8">
            <Zap size={14} />
            Open-source engineering simulation
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
            Simulate physics.
            <br />
            <span className="text-blue-500">Powered by AI.</span>
          </h1>

          <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10">
            Run structural, thermal, and fluid simulations in your browser.
            No $50K license. No 6-month training. Free and open-source.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/simulations/new"
              className="flex items-center gap-2 px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors"
            >
              Start simulating
              <ArrowRight size={18} />
            </Link>
            <a
              href="https://github.com/Vitalcheffe/flow"
              className="flex items-center gap-2 px-8 py-4 bg-white/5 border border-white/10 text-white rounded-xl font-semibold hover:bg-white/10 transition-colors"
            >
              <Github size={18} />
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-slate-900 mb-4">
            Everything you need to simulate
          </h2>
          <p className="text-slate-500 text-center max-w-2xl mx-auto mb-16">
            From classical FEA to AI-accelerated neural operators
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: Gauge,
                title: 'Structural Analysis',
                desc: 'Stress, strain, deformation under load. Beam, plate, and shell elements.',
              },
              {
                icon: Thermometer,
                title: 'Thermal Analysis',
                desc: 'Heat transfer, steady-state and transient. Conduction, convection.',
              },
              {
                icon: Waves,
                title: 'Fluid Dynamics',
                desc: 'Laminar CFD. Velocity and pressure fields. SIMPLE algorithm.',
              },
              {
                icon: Cpu,
                title: 'AI Solvers',
                desc: 'Neural Operators for 100x speed. Fourier Neural Operator architecture.',
              },
              {
                icon: Globe,
                title: 'Web-based',
                desc: 'No installation. Open browser, import geometry, simulate.',
              },
              {
                icon: Zap,
                title: 'Open Source',
                desc: 'MIT license. Self-hostable. API for automation.',
              },
            ].map((feature) => (
              <div
                key={feature.title}
                className="p-6 rounded-2xl border border-slate-200 hover:border-blue-200 hover:shadow-md transition-all"
              >
                <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center mb-4">
                  <feature.icon size={20} />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-500">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Comparison */}
      <section className="py-24 px-6 bg-slate-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-slate-900 mb-16">
            Why FLOW?
          </h2>

          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider border-b border-slate-100">
                  <th className="px-6 py-4">Feature</th>
                  <th className="px-6 py-4">ANSYS</th>
                  <th className="px-6 py-4">FreeCAD</th>
                  <th className="px-6 py-4 text-blue-600">FLOW</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {[
                  ['Price', '$50K+/year', 'Free', 'Free'],
                  ['Web-based', 'No', 'No', 'Yes'],
                  ['AI solver', 'No', 'No', 'Yes'],
                  ['Mobile', 'No', 'No', 'Yes'],
                  ['API', 'No', 'No', 'Yes'],
                  ['Self-host', 'No', 'N/A', 'Yes'],
                  ['Setup time', 'Weeks', 'Hours', 'Minutes'],
                ].map(([feature, ansys, freecad, flow]) => (
                  <tr key={feature as string}>
                    <td className="px-6 py-3 font-medium text-slate-900">{feature}</td>
                    <td className="px-6 py-3 text-sm text-slate-500">{ansys}</td>
                    <td className="px-6 py-3 text-sm text-slate-500">{freecad}</td>
                    <td className="px-6 py-3 text-sm font-medium text-blue-600">{flow}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">
            Ready to simulate?
          </h2>
          <p className="text-slate-500 mb-8">
            Open-source. Free forever. Start in minutes.
          </p>
          <Link
            to="/simulations/new"
            className="inline-flex items-center gap-2 px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors"
          >
            Create your first simulation
            <ArrowRight size={18} />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-slate-200">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <p className="text-sm text-slate-400">
            FLOW — Open-source engineering simulation with AI
          </p>
          <div className="flex items-center gap-4">
            <a href="https://github.com/Vitalcheffe/flow" className="text-slate-400 hover:text-slate-600">
              <Github size={20} />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
