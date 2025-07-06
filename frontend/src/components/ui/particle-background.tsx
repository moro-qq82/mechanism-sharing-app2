import React, { useEffect, useRef } from 'react';
import { Engine, Render, World, Bodies, Mouse, MouseConstraint, Body, Runner } from 'matter-js';

interface ParticleBackgroundProps {
  className?: string;
}

export const ParticleBackground: React.FC<ParticleBackgroundProps> = ({ 
  className = '' 
}) => {
  const sceneRef = useRef<HTMLDivElement>(null);
  const engineRef = useRef<Engine | null>(null);
  const renderRef = useRef<Render | null>(null);
  const runnerRef = useRef<Runner | null>(null);

  useEffect(() => {
    if (!sceneRef.current) return;

    // エンジンの作成
    const engine = Engine.create();
    engineRef.current = engine;

    // 重力をなくしてふわふわ動かす
    engine.world.gravity.y = 0;
    engine.world.gravity.x = 0;

    // 適切なサイズを取得
    const containerWidth = sceneRef.current.clientWidth || sceneRef.current.offsetWidth || 800;
    const containerHeight = sceneRef.current.clientHeight || sceneRef.current.offsetHeight || 100;

    // レンダラーの作成
    const render = Render.create({
      element: sceneRef.current,
      engine: engine,
      options: {
        width: containerWidth,
        height: containerHeight,
        wireframes: false,
        background: 'transparent',
        pixelRatio: window.devicePixelRatio || 1,
      }
    });
    renderRef.current = render;

    // 壁を作成（見えない境界）
    const walls = [
      Bodies.rectangle(containerWidth / 2, -25, containerWidth, 50, { 
        isStatic: true,
        render: { visible: false }
      }),
      Bodies.rectangle(containerWidth / 2, containerHeight + 25, containerWidth, 50, { 
        isStatic: true,
        render: { visible: false }
      }),
      Bodies.rectangle(-25, containerHeight / 2, 50, containerHeight, { 
        isStatic: true,
        render: { visible: false }
      }),
      Bodies.rectangle(containerWidth + 25, containerHeight / 2, 50, containerHeight, { 
        isStatic: true,
        render: { visible: false }
      })
    ];

    // 粒子を作成
    const particles: Body[] = [];
    const particleCount = 15;
    const width = containerWidth;
    const height = containerHeight;
    
    for (let i = 0; i < particleCount; i++) {
      const x = Math.random() * width;
      const y = Math.random() * height;
      const baseRadius = 12; // 基準サイズを3倍に（4 × 3 = 12）
      const radius = baseRadius * (0.8 + Math.random() * 0.4); // 0.8〜1.2倍の範囲
      
      // 確実に見える明るい色を使用
      const colors = [
        '#FF6B6B', // 明るい赤
        '#4ECDC4', // 明るいティール
        '#45B7D1', // 明るい青
        '#96CEB4', // 明るい緑
        '#FFEAA7', // 明るい黄
        '#DDA0DD', // 明るい紫
        '#98D8C8', // 明るいミント
        '#F7DC6F'  // 明るいゴールド
      ];
      
      const color = colors[i % colors.length];
      
      const particle = Bodies.circle(x, y, radius, {
        restitution: 0.2,
        friction: 0.2,
        frictionAir: 0.08,
        density: 0.0001,
        render: {
          fillStyle: color,
          strokeStyle: '#FFFFFF',
          lineWidth: 2,
        }
      });

      // 非常にゆっくりとした初期速度を与える
      Body.setVelocity(particle, {
        x: (Math.random() - 0.5) * 0.5,
        y: (Math.random() - 0.5) * 0.5
      });

      particles.push(particle);
    }

    // マウス制御を追加
    const mouse = Mouse.create(render.canvas);
    const mouseConstraint = MouseConstraint.create(engine, {
      mouse: mouse,
      constraint: {
        stiffness: 0.2,
        render: {
          visible: false
        }
      }
    });

    // ワールドに追加
    World.add(engine.world, [...walls, ...particles, mouseConstraint]);

    // canvasスタイルを設定
    if (render.canvas) {
      render.canvas.style.position = 'absolute';
      render.canvas.style.top = '0';
      render.canvas.style.left = '0';
      render.canvas.style.width = '100%';
      render.canvas.style.height = '100%';
      render.canvas.style.pointerEvents = 'auto';
      render.canvas.style.zIndex = '5';
    }

    // レンダリング開始
    Render.run(render);
    
    // Runnerを作成してエンジンを実行
    const runner = Runner.create({
      delta: 16.666, // 60 FPS
      isFixed: true
    });
    runnerRef.current = runner;
    Runner.run(runner, engine);

    // 各パーティクルの目標位置を管理
    const particleTargets = particles.map(particle => ({
      targetX: particle.position.x + (Math.random() - 0.5) * 100,
      targetY: particle.position.y + (Math.random() - 0.5) * 100,
      lastUpdate: Date.now()
    }));

    // 滑らかで継続的な動きを適用
    const applyGentleForces = () => {
      particles.forEach((particle, index) => {
        const target = particleTargets[index];
        const now = Date.now();
        
        // 5秒ごとに新しい目標位置を設定
        if (now - target.lastUpdate > 5000) {
          target.targetX = Math.random() * containerWidth;
          target.targetY = Math.random() * containerHeight;
          target.lastUpdate = now;
        }
        
        // 現在位置から目標位置への方向を計算
        const dx = target.targetX - particle.position.x;
        const dy = target.targetY - particle.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // 目標位置に近づくための非常に小さなフォースを適用
        if (distance > 10) {
          const forceStrength = 0.000008;
          const force = {
            x: (dx / distance) * forceStrength,
            y: (dy / distance) * forceStrength
          };
          Body.applyForce(particle, particle.position, force);
        }
        
        // 速度制限（最大速度を1に制限してよりゆっくりに）
        const currentSpeed = Math.sqrt(
          particle.velocity.x * particle.velocity.x + 
          particle.velocity.y * particle.velocity.y
        );
        
        if (currentSpeed > 1) {
          const factor = 1 / currentSpeed;
          Body.setVelocity(particle, {
            x: particle.velocity.x * factor,
            y: particle.velocity.y * factor
          });
        }
      });
    };

    const forceInterval = setInterval(applyGentleForces, 100); // より頻繁に、より小さなフォースを適用

    // クリーンアップにフォース間隔も追加
    const originalCleanup = () => {
      clearInterval(forceInterval);
      window.removeEventListener('resize', handleResize);
      
      if (runnerRef.current) {
        Runner.stop(runnerRef.current);
      }
      
      if (renderRef.current) {
        Render.stop(renderRef.current);
        if (renderRef.current.canvas) {
          renderRef.current.canvas.remove();
        }
      }
      
      if (engineRef.current) {
        Engine.clear(engineRef.current);
      }
    };

    // リサイズ処理
    const handleResize = () => {
      if (sceneRef.current && render) {
        render.canvas.width = sceneRef.current.clientWidth;
        render.canvas.height = sceneRef.current.clientHeight;
        render.options.width = sceneRef.current.clientWidth;
        render.options.height = sceneRef.current.clientHeight;
      }
    };

    window.addEventListener('resize', handleResize);

    // クリーンアップ
    return originalCleanup;
  }, []);

  return (
    <div 
      ref={sceneRef} 
      className={`absolute inset-0 z-0 ${className}`}
      style={{ 
        width: '100%', 
        height: '100%',
        overflow: 'hidden',
        pointerEvents: 'auto'
      }}
    />
  );
};