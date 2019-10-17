function trajectory = trajectory_following(refx, refy)
% trajectory following in the presence of disturbance
% dimension
%addpath('/Users/chrislaw/Box Sync/Research/Zero_Opt2019/Learn2Opt/p_poly_dist')


nx = 3;
nc = 2;
do_plot = 0;
% horizon
K = 5;
% actuator limits
uMax = [5; pi];
uMin = [0.1; -pi];

x6 = [7, 9, 9, 7; 10, 12, 12, 10];
y6 = [4, 4, 6, 6; 12, 12, 14, 14];

% obstacle 

% dataset
deltaT = 1;
% ref = [0.71, 0.1, 0; 0.7, 0.2, 0; 0.65, 0.22, 0; 0.55, 0.25, 0; 0.47, 0.31, 0; 0.39, 0.36, 0;
%     0.35, 0.39, 0; 0.28, 0.45, 0; 0.21, 0.49, 0; 0.2, 0.5, 0; 0.19, 0.55, 0; 0.19, 0.62, 0; 
%     0.17, 0.71, 0; 0.17, 0.71, 0]'*10;
% ref1 = [0.3, 0; 0.34, 0.09; 0.38, 0.18; 0.44, 0.27; 0.49, 0.35; 0.54, 0.44;
%     0.56, 0.48; 0.59, 0.56; 0.62, 0.66; 0.63, 0.71; 0.65, 0.79; 0.68, 0.89;
%     0.68, 0.89]' * 20;
% ref1 = [0.3, 0; 0.34, 0.09; 0.35, 0.19; 0.37, 0.29; 0.39, 0.33; 0.41, 0.42;
%     0.44, 0.51; 0.46, 0.57; 0.5, 0.65; 0.57, 0.73; 0.61, 0.78; 0.67, 0.86; 
%     0.67, 0.86]'*20;
% refx = [0.0,
%  -0.12291657333596531,
%  5.5987874198873415,
%  7.264846969340003,
%  6.377822476382649,
%  7.85092975765561,
%  9.26557283248189,
%  10.598016619197303,
%  12.282882167771836,
%  15.676076196754183,
%  17.816797045884616,
%  18.66939739043501,
%  18.776074816798946,
%  19.791994778682017,
%  20.0]';
% 
% refy = [0.0,
%  -0.8056469376614854,
%  0.6821548510509632,
%  4.632259700313473,
%  5.884467756129742,
%  6.698670993092066,
%  8.246773430638678,
%  11.2337450122686,
%  13.275795844887735,
%  13.944569635432543,
%  15.716435429040285,
%  16.308751843861803,
%  19.86871543520798,
%  19.603291705108592,
%  20.0]';

ref1 = [refx; refy];

ref = ref1(:,1);
space = 1;
for s = 1: size(ref1, 2)-1
    for s1 = 1:space
        ref(:, space*(s-1)+s1+1) = ref1(:, s) + s1 * (ref1(:,s+1)-ref1(:,s))/space;
    end
end
ref(:, end+1:end+K-1) = repmat(ref(:, end), 1, K-1);   % K-1 final states
ref(3, :) = zeros(1, size(ref, 2));
Q = diag(repmat([25;25],K,1));
R = diag(repmat([10; 1],K,1));  % the weighting matrices are important
% true initial state
x0 = ref(:, 1);  % [2,-0.5,0.1]'; 
% predicted input sequence
u0 = zeros(K*nc, 1);

horizon = length(ref) - (K-1);
opts = optimoptions(@fmincon,'Algorithm','interior-point', 'Display', 'off');  % 'sqp'
trajectory = zeros(nx, horizon);
control = zeros(nc, horizon-1);
trajectory(:, 1) = x0;
for k = 1:horizon-1
%     disp(k)
    % current state is at time step k
    xRef = ref(1:2, k+1:k+K);
%     tstart = tic;
    [u, ~, ~, ~] = fmincon(@(u)objective(u, xRef, Q, R, x0, nx, nc, K, deltaT, x6, y6),u0,[], ...
    [],[],[],[],[], @(u)ineq_constraint(u, uMax, uMin, K), opts);
%     telapsed = toc(tstart);
    % next true state after applying the first input
    x0 = true_model(x0, u(1:nc, 1), deltaT);
    % next initial guess
    u0 = [u(nc+1:end, :); u((K-1)*nc+1:end, :)];
    % save current state
    trajectory(:, k+1) = x0; 
    control(:, k) = u(1:nc, 1);
%     disp(['current time step: ', int2str(k)])
end
% 
if do_plot == 1
    figure
    hold on
%     for h = 1:5
%         plot(human{h, 1}, human{h, 2});
%     end
    for k=1:size(x6, 1)
        plot([x6(k,:), x6(k,1)], [y6(k,:), y6(k,1)])
    end
    plot(ref(1,:), ref(2,:), 'bo-', 'markersize', 5);
%     plot(ref1(1,1), ref1(2,1), 'go', 'markersize', 10);
%     plot(ref1(1,end), ref1(2,end), 'go', 'markersize', 10);
%     axis([0 20 0 20])
    plot(trajectory(1,:), trajectory(2,:), 'ro-', 'markersize', 5);
    % plot(ref(1,1:len), ref(2,1:len), 'linewidth', 2)
    legend('reference trajectory', 'MPC trajectory')

%     figure
%     plot(trajectory(1,:)-ref(1,1:horizon), 'linewidth', 2)
%     hold on 
%     plot(trajectory(2,:)-ref(2,1:horizon), 'linewidth', 2)
%     figure
%     hold on 
%     plot(control(1,:), 'linewidth', 2)
%     plot(control(2,:), 'linewidth', 2)
end



    function J = objective(u, xRef, Q, R, x0, nx, nc, K, deltaT, xv, yv)
    % Input
    % xRef      -- reference trajectory,   dim: [K*nx; 1]
    % uRef      -- reference input signal, dim: [K*nc; 1]
    % xMean     --  true state,            dim: [nx; 1]
    % u         -- reference input signal, dim: [K*nc; 1]
    % Q, R      -- cost matrix
    % nx        -- dimension of states
    % nc        -- dimension of inputs
    % K         -- prediction horizon
    % Output
    % objective value
    
    x = zeros(nx, K+1);
    x(:, 1) = x0;
    for i = 1:K
        x(:, i+1) = true_model(x(:, i), u((i-1)*nc+1:i*nc, 1), deltaT);
    end
    x = x(1:2, 2:end);
    penalty_obs = obs_avoid(x, xv, yv);
    x = x(:);
%     penalty_goal = goal_oriented(x, ref1(:, end));
    J = (xRef(:) - x)' * Q * (xRef(:) - x) + 100 * penalty_obs ...
            + u' * R * u;  % + 1/2 * penalty_goal;
%          + u' * R * u + (xRef0(:) - x)' * 0.1 * Q * (xRef0(:) - x);
    end

    function [c, ceq] = ineq_constraint(u, uMax, uMin, K)
    % Input
    % u      -- control,          dim: [K*nc; 1]
    % uMax   -- maximum input,    dim: scalar
    % uMin   -- minimum input,    dim: scalar
    % Output
    % c      -- constraint

    % constraints on inputs
    c = -[repmat(uMax,K,1) - u;  u - repmat(uMin,K,1)];
    ceq = [];
    end

    function x = true_model(x0, u, deltaT)
	% known model
        theta = x0(end);
        B = [cos(theta) 0; sin(theta) 0; 0 1];
        x = x0 + deltaT*B*u;
    end

%     function penalty_obs = obs_avoid(p, xv, yv)
%         epsilon = 1e-8;
%         penalty_obs = 0;
%         for m = 1:size(xv, 1)
%             [d_min, ~, ~, ~, ~, ~, ~, ~, ~, ~] = test_p_poly_dist(p(1,:), p(2,:), xv(m,:), yv(m,:), true);
%             penalty_obs =  penalty_obs + sum(1./(abs(d_min) + epsilon));
%         end
%         
%     end

    function penalty_obs = obs_avoid(x, xv, yv)
        penalty_obs = 0;
        epsilon = 1e-8;
        n = 3;
        xp = [];
        yp = [];
        for i = 1:size(x,2)-1
            xp = [xp, x(1,i) + [0:n] * (x(1,i+1)-x(1,i))/(n+1)];
            yp = [yp, x(2,i) + [0:n] * (x(2,i+1)-x(2,i))/(n+1)];
        end
        for m = 1:size(xv, 1)
            [d_min, ~, ~, ~, ~, ~, ~, ~, ~, ~] = test_p_poly_dist(xp, yp, xv(m,:), yv(m,:), true);
            penalty_obs =  penalty_obs + sum(1./(abs(d_min) + epsilon));
        end
    end
end
