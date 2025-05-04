function u = mpc_controller(state, goal_state, obstacles, N, dt, V_current, psi_current)
    % ==== 完整版 AN-MPC优化器 (Fossen简化 + 动态权重Q + 水流补偿 + 禁区避障 + 期望速度航向) ====

    best_cost = inf;
    best_u = [0, 0, 0];

    ax_range = -0.3:0.1:0.3;
    ay_range = -0.3:0.1:0.3;
    omega_range = -0.15:0.05:0.15;


    % 动态权重调整参数
    alpha = 2;  
    beta  = 2;
    gamma = 0.3;


    for ax = ax_range
        for ay = ay_range
            for omega = omega_range

                pred = state;  % 每个动作组合，从当前状态开始预测
                cost = 0;

                for k = 1:N
                    % === 动态目标方向与速度 ===
                    dx = goal_state(1) - pred(1);
                    dy = goal_state(2) - pred(2);
                    theta_target = atan2(dy, dx);
                    theta_diff = wrapToPi(theta_target - pred(3));
                    u_ref = 5.0 * cos(theta_diff);
                    v_ref = 5.0 * sin(theta_diff);
                    theta_ref = theta_target;

                    % ==== 动力学预测 ====
                    pred(4) = pred(4) + ax * dt;
                    pred(5) = pred(5) + ay * dt;
                    pred(6) = pred(6) + omega * dt;

                    Xdot = pred(4) * cos(pred(3)) - pred(5) * sin(pred(3));
                    Ydot = pred(4) * sin(pred(3)) + pred(5) * cos(pred(3));

                    pred(1) = pred(1) + Xdot * dt;
                    pred(2) = pred(2) + Ydot * dt;
                    pred(3) = pred(3) + pred(6) * dt;

                    % ==== 动态生成Q矩阵 ====
                    speed_sq = pred(4)^2 + pred(5)^2;
                  Q_diag = [
                     1 + alpha * speed_sq;        % X方向位置误差权重
                     1 + beta  * speed_sq;         % Y方向位置误差权重
                     1 / (1 + gamma * speed_sq);   % 航向角误差权重
                     1         % 纵向速度误差权重
                     1         % 横向速度误差权重
                     1         % 航向角速度误差权重
                            ];
                    Q = diag(Q_diag);

                    % ==== 累积代价函数 ====

                    % 1. 轨迹误差（6维状态）
                    delta_state = pred(1:6) - goal_state(1:6);
                    cost = cost + delta_state' .* Q .* delta_state;

                    % 2. 控制能耗（推力消耗）
                    cost = cost + 0.2 * (ax^2 + ay^2 + omega^2);

                    % 3. 速度保持项（与期望u_ref, v_ref比较）
                    cost = cost + 0.2 * ((pred(4) - u_ref)^2 + (pred(5) - v_ref)^2);

                    % 4. 航向角跟踪项（与期望theta_ref比较）
                    cost = cost + 0.3 * (pred(3) - theta_ref)^2;
                    % ==== 新增：接近目标时鼓励航向角对准目标方向 ====
                    distance_to_goal = norm(pred(1:2) - goal_state(1:2));
                    if distance_to_goal < 10.0
                        theta_goal_ref = atan2(goal_state(2) - pred(2), goal_state(1) - pred(1));
                        cost = cost + 0.6 * (pred(3) - theta_goal_ref)^2; % 航向对准奖励
                    end
                    
                    % 5. 水流补偿项（期望抵消水流带来的漂移）
                    if nargin >= 6
                        ex = pred(1) - goal_state(1);
                        ey = pred(2) - goal_state(2);
                        cost = cost + 0.05 * (V_current * cos(psi_current) * ex + V_current * sin(psi_current) * ey)^2;
                    end

                    % 6. 禁区避障检测
                    for i = 1:length(obstacles)
                        obs = obstacles{i};
                        if inpolygon(pred(1), pred(2), obs(:,1), obs(:,2))
                            cost = cost + 30000; % 惩罚项目
                        end
                    end
                end

                % ==== 更新最优动作 ====
                if cost < best_cost
                    best_cost = cost;
                    best_u = [ax, ay, omega];
                end

            end
        end
    end

    u = best_u;
end
