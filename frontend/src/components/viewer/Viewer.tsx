import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Environment } from '@react-three/drei';
import * as THREE from 'three';

interface BeamProps {
  length: number;
  height: number;
  color?: string;
  wireframe?: boolean;
}

const Beam: React.FC<BeamProps> = ({ length, height, color = '#3B82F6', wireframe = false }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  return (
    <mesh
      ref={meshRef}
      position={[length / 2, height / 2, 0]}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <boxGeometry args={[length, height, 0.05]} />
      <meshStandardMaterial
        color={hovered ? '#60A5FA' : color}
        wireframe={wireframe}
        metalness={0.3}
        roughness={0.6}
      />
    </mesh>
  );
};

interface PlateProps {
  width: number;
  height: number;
  temperature?: number[][];
  colorMap?: (value: number) => string;
}

const Plate: React.FC<PlateProps> = ({ width, height, temperature }) => {
  const meshRef = useRef<THREE.Mesh>(null);

  return (
    <mesh ref={meshRef} position={[width / 2, height / 2, 0]} rotation={[0, 0, 0]}>
      <boxGeometry args={[width, height, 0.02]} />
      <meshStandardMaterial
        color="#10B981"
        metalness={0.2}
        roughness={0.7}
      />
    </mesh>
  );
};

interface ViewerProps {
  type?: 'beam' | 'plate';
  length?: number;
  height?: number;
  showGrid?: boolean;
  showAxes?: boolean;
  temperature?: number[][];
}

const Viewer: React.FC<ViewerProps> = ({
  type = 'beam',
  length = 1.0,
  height = 0.1,
  showGrid = true,
  showAxes = true,
  temperature,
}) => {
  return (
    <div className="w-full h-full bg-slate-900 rounded-2xl overflow-hidden">
      <Canvas
        camera={{ position: [length, height * 3, length], fov: 50 }}
        shadows
      >
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 5, 5]} intensity={0.8} castShadow />
        <pointLight position={[-5, 5, -5]} intensity={0.3} />

        {type === 'beam' && <Beam length={length} height={height} />}
        {type === 'plate' && (
          <Plate width={length} height={height} temperature={temperature} />
        )}

        {showGrid && (
          <Grid
            args={[5, 5]}
            cellSize={0.1}
            cellThickness={0.5}
            cellColor="#334155"
            sectionSize={1}
            sectionThickness={1}
            sectionColor="#475569"
            fadeDistance={10}
            position={[0, 0, 0]}
          />
        )}

        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={0.5}
          maxDistance={10}
        />
      </Canvas>
    </div>
  );
};

export default Viewer;
